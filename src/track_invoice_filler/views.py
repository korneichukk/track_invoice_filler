from django.forms import formset_factory
import os
from pathlib import Path
from datetime import timedelta, datetime
import sys
import threading
import logging

from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.views import login_required
from django.http import FileResponse, Http404

from .forms import CompanyInfoForm, TrackInvoiceForm
from .track_invoice_filler import fill_pdf_by_coordinates, name_pdf_template_map, coordinates

TrackInvoiceFormSet = formset_factory(TrackInvoiceForm, extra=1, max_num=5)

def index(request):
    return render(request, "index.html")

def download_pdf(request, company_name, template_name):
    file_path = settings.MEDIA_ROOT / company_name / template_name

    if not file_path.exists():
        raise Http404("File not found")

    try:
        return FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename=template_name,
        )
    except Exception as e:
        raise Http404(f"Error downloading file: {str(e)}")

def delete_old_files(file_paths):
    current_time = timezone.now()
    for file_path in file_paths:
        if file_path.exists():
            file_mod_time = timezone.make_aware(
                datetime.fromtimestamp(file_path.stat().st_mtime)
            )
            file_age = current_time - file_mod_time
            logging.info(
                f"File: {file_path}, Last Modified: {file_mod_time}, Age: {file_age}"
            )

            # Check if the file is older than 1 minute
            if file_age > timedelta(minutes=10):
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted old file: {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")
            else:
                logging.info(f"File not old enough to delete: {file_path}")
        else:
            logging.warning(f"File does not exist: {file_path}")


@login_required
def create_track_invoice(request):
    if request.method == "POST":
        company_form = CompanyInfoForm(request.POST)
        formset = TrackInvoiceFormSet(request.POST)

        templates_and_links = []
        generated_files = []

        if company_form.is_valid() and formset.is_valid():
            company_info = company_form.cleaned_data
            invoices_data = [form.cleaned_data for form in formset]

            template_name = name_pdf_template_map[len(invoices_data)]
            path_to_template = settings.BASE_DIR / "applications" / template_name

            path_to_save_dir = Path(settings.MEDIA_ROOT / company_info["company_name"])
            path_to_save_dir.mkdir(parents=True, exist_ok=True)

            fill_pdf_by_coordinates(
                path_to_template,
                path_to_save_dir / template_name,
                {"company": company_info, "invoices": invoices_data},
                coordinates["default_invoice"]
            )

            download_link = os.path.join(
                    settings.MEDIA_URL, company_info["company_name"], template_name
                )

            templates_and_links.append((template_name, download_link))
            generated_files.append(path_to_save_dir / template_name)

            def delete_files_later():
                threading.Timer(600, delete_old_files, [generated_files]).start()

            delete_files_later()


            return render(request, "success.html", {"templates_and_links": templates_and_links, "company_name": company_info["company_name"]}
            )
    else:
        company_form = CompanyInfoForm()
        formset = TrackInvoiceFormSet()

    return render(request, "create_track_invoice.html", {
        "company_form": company_form,
        "formset": formset
    })

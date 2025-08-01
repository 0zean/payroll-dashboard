import reflex as rx
import httpx

from ..backend.api_routes import clear_payroll, url_base


class IndexState(rx.State):
    """The index state class."""

    download_loading: bool = False
    clear_loading: bool = False

    @rx.event
    async def start_download(self):
        self.download_loading = True
        yield type(self).finish_download()

    @rx.event
    async def finish_download(self):
        try:
            response = httpx.get(f"{url_base}download-payroll")

            if response.status_code != 200:
                raise Exception("Failed to fetch file")

            yield rx.download(filename="payroll.xlsx", data=response.content)
            self.download_loading = False
            yield rx.toast.success("Downloaded payroll!", position="top-center")
        except Exception as e:
            self.download_loading = False
            yield rx.toast.error(f"Error downloading payroll: {e}", position="top-center")

    @rx.event
    async def start_clean(self):
        self.clear_loading = True
        yield type(self).finish_clean()

    @rx.event
    async def finish_clean(self):
        try:
            await clear_payroll()
            self.clear_loading = False
            yield rx.toast.success("Cleared payroll!", position="top-center")
        except Exception as e:
            self.clear_loading = False
            yield rx.toast.error(f"Error clearing payroll: {e}", position="top-center")

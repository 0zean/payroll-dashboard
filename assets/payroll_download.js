async function triggerPayrollDownload(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Failed to download file");
        }

        const contentDisposition = response.headers.get("Content-Disposition");
        let filename = "payroll.xlsx";  // fallback filename

        // Extract filename from header if present
        if (contentDisposition && contentDisposition.includes("filename=")) {
            filename = contentDisposition
                .split("filename=")[1]
                .replace(/['"]/g, "");
        }

        const blob = await response.blob();
        const urlBlob = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = urlBlob;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(urlBlob); // clean up
    } catch (error) {
        console.error("Download error:", error);
        alert("Download failed");
    }
}


const modal = document.getElementById("share-modal");

function openShareEditor(shareId, expiry) {
    document.getElementById("share-id").value = shareId;
    document.getElementById("share-expiry").value = expiry;
    document.getElementById("share-message").hidden = true;
    modal.hidden = false;
}

function closeShareEditor() {
    modal.hidden = true;
}

document.getElementById("share-form")?.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const shareId = document.getElementById("share-id").value;
        const expiry = document.getElementById("share-expiry").value;
        const message = document.getElementById("share-message");
        const button = event.submitter;

        button.disabled = true;
        button.textContent = "Saving…";

        try {
            const response = await fetch(`/share/${shareId}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ expiry })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Unable to save changes");
            }

            message.textContent = "Share settings saved successfully.";
            message.className = "form-message success-message";
            message.hidden = false;

            setTimeout(() => window.location.reload(), 700);
        } catch (error) {
            message.textContent = error.message;
            message.className = "form-message error-message";
            message.hidden = false;
        } finally {
            button.disabled = false;
            button.textContent = "Save changes";
        }
    }
);

modal?.addEventListener("click", (event) => {
    if (event.target === modal) {
        closeShareEditor();
    }
});

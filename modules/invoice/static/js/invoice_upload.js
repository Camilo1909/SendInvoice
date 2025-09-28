$(document).ready(function () {
    const $dropArea = $("#drop-area");
    const $inputFile = $("#invoice-image");
    const $preview = $("#preview");

    function showPreview(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            $preview.attr("src", e.target.result).removeClass("d-none");
        };
        reader.readAsDataURL(file);
    }

    // Click sobre el área => abrir file input
    $dropArea.on("click", function () {
        $inputFile.trigger("click");
    });

    // Drag & Drop
    $dropArea.on("dragover", function (e) {
        e.preventDefault();
        $dropArea.addClass("bg-secondary text-white");
    });

    $dropArea.on("dragleave", function () {
        $dropArea.removeClass("bg-secondary text-white");
    });

    $dropArea.on("drop", function (e) {
        e.preventDefault();
        $dropArea.removeClass("bg-secondary text-white");
        const files = e.originalEvent.dataTransfer.files;
        $inputFile[0].files = files;
        showPreview(files[0]);
    });

    // Input manual
    $inputFile.on("change", function () {
        if (this.files.length > 0) {
            showPreview(this.files[0]);
        }
    });

    // Copiar / Pegar
    $(document).on("paste", function (e) {
        const items = (e.originalEvent.clipboardData || e.clipboardData).items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf("image") !== -1) {
                const file = items[i].getAsFile();
                const dt = new DataTransfer();
                dt.items.add(file);
                $inputFile[0].files = dt.files;
                showPreview(file);
            }
        }
    });
});

window.onload = function () {
    document.getElementById("download-btn2").addEventListener("click", () => {
        const invoice = this.document.getElementById("main-div");
        console.log(invoice);
        console.log(window);
        var opt = {
            margin: 0.25,
            filename: "certificate.pdf",
            image: {
                type: "jpeg",
                quality: 0.98
            },
            jsPDF: {
                unit: "in",
                format: "letter",
                orientation: "portrait"
            },
        };
        html2pdf().from(invoice).set(opt).save();
    });
};
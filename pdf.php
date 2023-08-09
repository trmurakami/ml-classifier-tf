<!DOCTYPE html>
<html>

<head>
    <title>Extrair Texto de PDF</title>
    <script src="pdfjs/pdf.js"></script>
</head>

<body>
    <h1>Extrair Texto de PDF</h1>

    <form id="pdfForm">
        <input type="file" id="pdfInput" accept=".pdf">
        <button type="submit">Extrair Texto</button>
    </form>

    <div id="output">
        <h2>Texto Extraído:</h2>
        <pre id="text"></pre>
    </div>

    <script>
    document.getElementById('pdfForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const fileInput = document.getElementById('pdfInput');
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const arrayBuffer = event.target.result;
                const typedArray = new Uint8Array(arrayBuffer);

                // Carregar PDF usando pdf.js
                pdfjsLib.getDocument(typedArray).promise.then(function(pdf) {
                    const numPages = pdf.numPages;
                    let fullText = '';

                    // Extrair texto de cada página
                    const extractText = function(pageNumber) {
                        return pdf.getPage(pageNumber).then(function(page) {
                            return page.getTextContent().then(function(textContent) {
                                let pageText = '';

                                textContent.items.forEach(function(item) {
                                    pageText += item.str + ' ';
                                });

                                fullText += pageText;

                                if (pageNumber < numPages) {
                                    return extractText(pageNumber + 1);
                                } else {
                                    return fullText;
                                }
                            });
                        });
                    };

                    extractText(1).then(function(extractedText) {
                        const textElement = document.getElementById('text');
                        textElement.textContent = extractedText;
                    }).catch(function(error) {
                        console.error('Erro ao extrair texto:', error);
                    });
                }).catch(function(error) {
                    console.error('Erro ao carregar PDF:', error);
                });
            };

            reader.readAsArrayBuffer(file);
        }
    });
    </script>
</body>

</html>
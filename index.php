<!DOCTYPE html>
<html lang="pt-br" dir="ltr">

<head>
    <?php
        include('inc/meta-header.php');
    ?>
    <!-- Load TensorFlow.js -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
    <script src="pdfjs/pdf.js"></script>
    <title>Classificador - Ciência da Informação</title>
</head>

<body>
    <?php
        include('inc/ga.php'); 
    ?>
    <div class="jumbotron">
        <div class="container bg-light p-5 rounded mt-5">
            <h1 class="display-5">Classificador - Ciência da Informação</h1>

            <div class="ml-container">
                <label for="search" class="form-label">Digite título e resumo</label>
                <textarea class="form-control" id="userInput" rows="10"
                    placeholder="Digite um título e resumo em português"></textarea>
                <form id="pdfForm">
                    <div class="mb-3">
                        <label for="formFile" class="form-label">Ou insira um PDF</label>
                        <input class="form-control" type="file" id="pdfInput" accept=".pdf">
                        <button type="submit" class="btn btn-warning mt-4">Extrair Texto (Primeiro passo, caso tenha
                            optado por PDF)</button>
                    </div>
                </form>

                <div id="transform-button">
                    <button type="submit" class="btn btn-warning mt-4" id="transform-btn">Transformar
                        texto (Segundo passo)</button>
                </div>

                <div id="submit-button">
                    <button type="submit" class="btn btn-primary mt-4" id="predict-btn" disabled=True>Predict!</button>
                    <a href="<?php $_SERVER['PHP_SELF']; ?>" class="btn btn-warning mt-4">Recargar</a>

                </div>
            </div>

            <table id="predictions-table" class="table mt-5">
                <tr>
                    <th>Interação</th>
                    <th>Classe Mais Provável</th>
                    <th>Probabilidade</th>
                    <th>Top 10 Classes prováveis</th>
                </tr>
            </table>

            <p>Modelo testado no <a href="https://www.tensorflow.org/?hl=pt-br" target="_blank">Tensorflow</a> e
                utilizando o <a href="https://www.tensorflow.org/js?hl=pt-br" target="_blank">Tensorflow.js</a> para
                consulta no Browser</p>

        </div>
    </div>


    <script src="./index.js"></script>
    <script src="./loadpdf.js"></script>
    <script src="./transform.js"></script>
</body>

</html>
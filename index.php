<!DOCTYPE html>
<html lang="pt-br" dir="ltr">

<head>
    <?php
        include('inc/meta-header.php');
    ?>
    <!-- Load TensorFlow.js -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
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
                <textarea class="form-control" id="userInput" rows="6"
                    placeholder="Digite um título e resumo em português"></textarea>
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
                    <th>Top 5 Classes</th>
                </tr>
            </table>

        </div>
    </div>


    <script src="./index.js"></script>
</body>

</html>
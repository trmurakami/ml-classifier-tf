<?php
/**
 * Arquivo de classes e funções
 */

function divResponse($search, $category) {

    switch ($category) {
        case "NORMALIZACAO":
            $response = '
                <div class="card text-center">
                    <div class="card-header">
                        Você pesquisou por: '.$search.'
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">Normalização</h5>
                        <p class="card-text">A Biblioteca da ECA preparou uma página com os principais tópicos relacionados à normalização, visite:</p>
                        <a href="http://www3.eca.usp.br/biblioteca/servi%C3%A7os/normalizacao" class="btn btn-primary">Visitar página de normalização</a>
                    </div>
                </div>
            ';
            return $response;
            break;
        case 1:
            echo "i equals 1";
            break;
        default:
            echo 'Orientação ainda não criada para a categoria: '.$category.'';
            break;
    }

}

?>
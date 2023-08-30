let speechText;
let predictOutput;
let theButton;
let vocab;
let vocabPath = 'py/gen_helpers/tokenizer_dictionary.json';
let tokenizer;
let model;
let modelPath = 'py/Model_js/model.json';


// Defina o classNames em um escopo mais amplo, fora da função initialize
let classNames;

function loadJSON(callback) {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open('GET', 'py/gen_helpers/label_encoder.json', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            callback(JSON.parse(xhr.responseText));
        }
    };
    xhr.send(null);
}

function initialize() {
    loadJSON(function (data) {
        classNames = Object.entries(data);
        //console.log(classNames);
    });
}

window.onload = initialize;

// For some reason the L2 regularization in tf does not 
// connect to the L2 regularizer in tfjs
class L2 {
    static className = 'L2';
    constructor(config) {
       return tf.regularizers.l2(config)
    }
}
tf.serialization.registerClass(L2);

// load the tokenizer from json
async function loadTokenizer() {
    let tknzr = fetch(vocabPath).then(response => {
        return response.json();
    })
    return tknzr;
  }

// Load the model from json
async function loadModel() {
    const model = tf.loadLayersModel(modelPath);
    return model;
}

// tokenize function to convert input text to list of tokenized segments
function tokenize(text) {
    var split_text = text.split(' ');
    var tokens = [];
    split_text.forEach(element => {
        if (tokenizer[element] != undefined) {
            tokens.push(tokenizer[element]);
          }
    });
    // create a list of slices of the list of tokens
    let i = 0;
    tokenized_text_segments = [];
    while (i+255 < Math.max(tokens.length, 256)) {
        var new_slice = tokens.slice(i,i+256);
        while (new_slice.length < 256) {
            new_slice.push(0);
          }
        tokenized_text_segments.push(new_slice);
        i = i + 255;
    }
    return tokenized_text_segments;
  }

async function predictParty() {
    const prob = tf.tidy(() => {
        text = document.getElementById('userInput').value;
        text = JSON.stringify(text);
        var stopwords = ["de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "há", "nos", "já", "está", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas", "este", "fosse", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse", "estivéssemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse", "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", "houverão", "houveria", "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos",
        "teriam", "DE", "A", "O", "QUE", "E", "DO", "DA", "EM", "UM", "PARA", "É", "COM", "NÃO", "UMA", "OS", "NO", "SE", "NA", "POR", "MAIS", "AS", "DOS", "COMO", "MAS", "FOI", "AO", "ELE", "DAS", "TEM", "À", "SEU", "SUA", "OU", "SER", "QUANDO", "MUITO", "HÁ", "NOS", "JÁ", "ESTÁ", "EU", "TAMBÉM", "SÓ", "PELO", "PELA", "ATÉ", "ISSO", "ELA", "ENTRE", "ERA", "DEPOIS", "SEM", "MESMO", "AOS", "TER", "SEUS", "QUEM", "NAS", "ME", "ESSE", "ELES", "ESTÃO", "VOCÊ", "TINHA", "FORAM", "ESSA", "NUM", "NEM", "SUAS", "MEU", "ÀS", "MINHA", "TÊM", "NUMA", "PELOS", "ELAS", "HAVIA", "SEJA", "QUAL", "SERÁ", "NÓS", "TENHO", "LHE", "DELES", "ESSAS", "ESSES", "PELAS", "ESTE", "FOSSE", "DELE", "TU", "TE", "VOCÊS", "VOS", "LHES", "MEUS", "MINHAS", "TEU", "TUA", "TEUS", "TUAS", "NOSSO", "NOSSA", "NOSSOS", "NOSSAS", "DELA", "DELAS", "ESTA", "ESTES", "ESTAS", "AQUELE", "AQUELA", "AQUELES", "AQUELAS", "ISTO", "AQUILO", "ESTOU", "ESTÁ", "ESTAMOS", "ESTÃO", "ESTIVE", "ESTEVE", "ESTIVEMOS", "ESTIVERAM", "ESTAVA", "ESTÁVAMOS", "ESTAVAM", "ESTIVERA", "ESTIVÉRAMOS", "ESTEJA", "ESTEJAMOS", "ESTEJAM", "ESTIVESSE", "ESTIVÉSSEMOS", "ESTIVESSEM", "ESTIVER", "ESTIVERMOS", "ESTIVEREM", "HEI", "HÁ", "HAVEMOS", "HÃO", "HOUVE", "HOUVEMOS", "HOUVERAM", "HOUVERA", "HOUVÉRAMOS", "HAJA", "HAJAMOS", "HAJAM", "HOUVESSE", "HOUVÉSSEMOS", "HOUVESSEM", "HOUVER", "HOUVERMOS", "HOUVEREM", "HOUVEREI", "HOUVERÁ", "HOUVEREMOS", "HOUVERÃO", "HOUVERIA", "HOUVERÍAMOS", "HOUVERIAM", "SOU", "SOMOS", "SÃO", "ERA", "ÉRAMOS", "ERAM", "FUI", "FOI", "FOMOS", "FORAM", "FORA", "FÔRAMOS", "SEJA", "SEJAMOS", "SEJAM", "FOSSE", "FÔSSEMOS", "FOSSEM", "FOR", "FORMOS", "FOREM", "SEREI", "SERÁ", "SEREMOS", "SERÃO", "SERIA", "SERÍAMOS", "SERIAM", "TENHO", "TEM", "TEMOS", "TÉM", "TINHA", "TÍNHAMOS", "TINHAM", "TIVE", "TEVE", "TIVEMOS", "TIVERAM", "TIVERA", "TIVÉRAMOS", "TENHA", "TENHAMOS", "TENHAM", "TIVESSE", "TIVÉSSEMOS", "TIVESSEM", "TIVER", "TIVERMOS", "TIVEREM", "TEREI", "TERÁ", "TEREMOS", "TERÃO", "TERIA", "TERÍAMOS", "TERIAM"]
        text = text.replace(stopwords, "")
        var x = tokenize(text)
        x = model.predict(tf.tensor2d(x, [x.length, 256]));

        // x.mean(0).print();
        x = x.arraySync();
        // x = tf.mean(x);
        //x = x.arraySync();
        return x
    })

    function getMostProbableClass(probabilities) {
        const maxProbability = Math.max(...probabilities);
        const predictedClass = probabilities.indexOf(maxProbability);
        return predictedClass;
      }

// Função para encontrar as K classes mais prováveis
function getTopKClasses(probabilities, k) {
    const topK = probabilities
      .map((probability, index) => ({ probability, index }))
      .sort((a, b) => b.probability - a.probability)
      .slice(0, k);
    return topK.map((item) => item.index);
}


// Mostrar os resultados no HTML
const table = document.getElementById('predictions-table');

for (let i = 0; i < prob.length; i++) {
  const exampleProbabilities = prob[i];
  const mostProbableClass = getMostProbableClass(exampleProbabilities);
  const top5Classes = getTopKClasses(exampleProbabilities, 10);

  const row = table.insertRow();
  const exampleCell = row.insertCell(0);
  const mostProbableCell = row.insertCell(1);
  const probabilityCell = row.insertCell(2);
  const top3Cell = row.insertCell(3);

  exampleCell.innerHTML = `${i + 1}`;
  mostProbableCell.innerHTML = classNames[mostProbableClass][0];
  probabilityCell.innerHTML = '<div class="progress" role="progressbar" aria-label="Success example" aria-valuenow="'+exampleProbabilities[mostProbableClass].toFixed(2)*100+'" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar bg-success" style="width: '+exampleProbabilities[mostProbableClass].toFixed(2)*100+'%">'+exampleProbabilities[mostProbableClass].toFixed(2)*100+'%</div></div>'+exampleProbabilities[mostProbableClass].toFixed(4)+'';
  top3Cell.innerHTML = top5Classes.map((classIndex) => `${classNames[classIndex][0]} (${exampleProbabilities[classIndex].toFixed(4)})`).join('<br/> ');
}


}


function predictSpeech() {
    predictParty().then((x) => {});
}

async function init() {
    sampleSelction = document.getElementById('samples');

    predictOutput = document.getElementById('result');
    
    theButton = document.getElementById("predict-btn");

    theButton.innerHTML = `Loading...`;

    tokenizer = await loadTokenizer();

    theButton.innerHTML = `Loading......`;

    model = await loadModel();

    theButton.disabled = false;
    theButton.addEventListener("click", predictSpeech);
    
    theButton.innerHTML = `Predict! (This may take a moment...)`;
}

init();
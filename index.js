let speechText;
let predictOutput;
let theButton;
let vocab;
let vocabPath = 'py/keras/tokenizer_dictionary.json';
let tokenizer;
let model;
let modelPath = 'py/keras/Model_js/model.json';


// Defina o classNames em um escopo mais amplo, fora da função initialize
let classNames;

function loadJSON(callback) {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open('GET', 'py/keras/label_encoder.json', true);
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
        console.log(classNames);
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
    text = text.toLowerCase();
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
    while (i+100 < Math.max(tokens.length, 350)) {
        var new_slice = tokens.slice(i,i+350);
        while (new_slice.length < 350) {
            new_slice.push(0);
          }
        tokenized_text_segments.push(new_slice);
        i = i + 100;
    }
    return tokenized_text_segments;
  }

async function predictParty() {
    const prob = tf.tidy(() => {
        text = document.getElementById('userInput').value;
        text = JSON.stringify(text);

        var stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"];
        text = text.replace(stopwords, "")
        var x = tokenize(text)
        x = model.predict(tf.tensor2d(x, [x.length, 350]));

        x.mean(0).print();
        x = x.arraySync();
        // x = tf.mean(x);
        //x = x.arraySync();
        return x
    })
    // const classNames = ['SDG01', 'SDG02', 'SDG03', 'SDG04', 'SDG05', 'SDG06', 'SDG07', 'SDG08', 'SDG09', 'SDG10', 'SDG11', 'SDG12', 'SDG13', 'SDG14', 'SDG15', 'SDG16'];

    //const classNames = require('py/keras/label_encoder.json');

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
  const top3Classes = getTopKClasses(exampleProbabilities, 3);

  const row = table.insertRow();
  const exampleCell = row.insertCell(0);
  const mostProbableCell = row.insertCell(1);
  const probabilityCell = row.insertCell(2);
  const top3Cell = row.insertCell(3);

  exampleCell.innerHTML = `${i + 1}`;
  mostProbableCell.innerHTML = classNames[mostProbableClass];
  probabilityCell.innerHTML = '<div class="progress" role="progressbar" aria-label="Success example" aria-valuenow="'+exampleProbabilities[mostProbableClass].toFixed(2)*100+'" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar bg-success" style="width: '+exampleProbabilities[mostProbableClass].toFixed(2)*100+'%">'+exampleProbabilities[mostProbableClass].toFixed(2)*100+'%</div></div>'+exampleProbabilities[mostProbableClass].toFixed(4)+'';
  top3Cell.innerHTML = top3Classes.map((classIndex) => `${classNames[classIndex]} (${exampleProbabilities[classIndex].toFixed(4)})`).join(', ');
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
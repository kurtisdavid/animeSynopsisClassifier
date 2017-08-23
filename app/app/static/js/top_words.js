
function findTopWords(element, top_words) {

  var class_ = $(element).attr('class').split(' ').pop();
  var class_words = top_words[class_.replace(/_/g, ' ')];
  var map = {};

  for (i = 0; i < class_words.length; i++) { 

    var tokens = class_words[i].split(' ');
    
    for (j = 0; j < tokens.length; j++) {

        if (!(tokens[j] in map)) {
            $('.synopsis').highlight(tokens[j], class_);
            map[tokens[j]]=1;

        }


    }

  }
}
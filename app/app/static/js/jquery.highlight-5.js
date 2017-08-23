/*

highlight v5

Highlights arbitrary terms.

<http://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html>

MIT license.

Johann Burkard
<http://johannburkard.de>
<mailto:jb@eaio.com>
~~~~~~~~~~~~~~~~~~~~~~~~~~
EDIT:

-Changed highlight to add a certain class to choose highlight color.
-FIXED nested highlights issue by calling removeHighlight on the child itself.
-Changed highlight to only highlight single letters when they are alone (useful for the feature R)

Kurtis David

*/
last_class = null;

jQuery.fn.highlight = function(pat, class_) {
 function innerHighlight(node, pat) {
  var skip = 0;
  if (node.nodeType == 3) {
   var pos = node.data.toUpperCase().indexOf(pat);
   pos -= (node.data.substr(0, pos).toUpperCase().length - node.data.substr(0, pos).length);
   if (pos >= 0) {
    // quality of life change to not highlight single letters UNLESS its a token itself (does not have alpha characters right before and after it)
    if (!(pat.length==1 && (node.data.charAt(pos+1).toUpperCase()!=node.data.charAt(pos+1)||(pos>0 && node.data.charAt(pos-1).toUpperCase()!=node.data.charAt(pos-1))))){
      var spannode = document.createElement('span');
      spannode.className = 'highlight ' + class_;
      var middlebit = node.splitText(pos);
      var endbit = middlebit.splitText(pat.length);
      var middleclone = middlebit.cloneNode(true);
      spannode.appendChild(middleclone);
      middlebit.parentNode.replaceChild(spannode, middlebit);
      skip = 1;
    }
   }
  }
  else if (node.nodeType == 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
   for (var i = 0; i < node.childNodes.length; ++i) {
    i += innerHighlight(node.childNodes[i], pat);
   }
  }
  return skip;
 }
 return this.length && pat && pat.length ? this.each(function() {
  innerHighlight(this, pat.toUpperCase());
 }) : this;
};

jQuery.fn.removeHighlight = function() {
 return $(this).find("span.highlight").each(function() {
  if (this.parentNode == null && this.childNode == null) {
    return
  } else if (this.children.length != 0){
    $(this).removeHighlight();
  }
  with (this.parentNode){
    replaceChild(this.firstChild,this);
    normalize();
  }
 });
};

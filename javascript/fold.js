/*
    Projet: GooDoc
    Fichier: style.js
    Auteur: Hugo

    Ce fichier presente des animations simple pouvant être ajouté au fichier HTML générés.
*/

function toggle(method_title){
    var docstring = method_title.nextElementSibling;

    if (getComputedStyle(docstring).display == "none"){
        unfold(docstring);
    }
    else{
        fold(docstring);
    }
}


function fold(element){
    element.style.display= "none";
}

function unfold(element){
    element.style.display="block";
}


function foldAll(){
    var title_array = document.querySelectorAll(".methods td:last-child");

    for(var i = 0; i<title_array.length; i++){
        fold(title_array[i]);
    }
}
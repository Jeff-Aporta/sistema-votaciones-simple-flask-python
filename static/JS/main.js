window.onload = function () {
  ocultarCortinaCarga()
};

setTimeout(() => {
  ocultarCortinaCarga()
}, 10*1000);

function ocultarCortinaCarga(){
  try {
    document.getElementById("ocultar").style.animation = "fadeOut";
    document.getElementById("ocultar").style.animationDuration = "0.5s";
    document.getElementById("ocultar").style.animationFillMode =  "forwards";
    setTimeout(() => {
      document.getElementById("ocultar").style.visibility = "hidden";
    }, 600);
  } catch (error) {
    console.log(error)
  }
}

function fireClickEvent(element) {
  var evt = new window.MouseEvent("click", {
    view: window,
    bubbles: true,
    cancelable: true,
  });
  element.dispatchEvent(evt);
}

function openurl(url, absolute = true, newtab = false) {
  var a = document.createElement("a");
  if (newtab) {
    a.target = "_blank";
  }
  if (absolute) {
    a.href = url;
  } else {
    a.href = getURLabsolute(url);
  }
  fireClickEvent(a);
}

async function iniciarBusqueda() {
  let { value: busqueda } = await Swal.fire({
    title: "Busqueda",
    input: "text",
    inputLabel: "Your IP address",
    showCancelButton: true,
    inputValidator: (value) => {
      if (!value) {
        return "You need to write something!";
      }
    },
  });
}

function getURLabsolute(string,static = false) {
  return getRootWebSitePath() + (static?"static/":"") + string;
}

function getRootWebSitePath() {
  var _location = document.location.toString();
  var applicationNameIndex = _location.indexOf(
    "/",
    _location.indexOf("://") + 3
  );
  var applicationName = _location.substring(0, applicationNameIndex) + "/";
  return applicationName;
}

function readText(ruta_local) {
  var texto = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", ruta_local, false);
  xmlhttp.send();
  if (xmlhttp.status == 200) {
    texto = xmlhttp.responseText;
  }
  return texto;
}

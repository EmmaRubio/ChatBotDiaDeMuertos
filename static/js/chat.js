const mensajes = document.getElementById("mensajes");
const input = document.getElementById("mensaje");
const boton = document.getElementById("btnEnviar");

function agregarMensaje(texto, tipo){

    const mensaje = document.createElement("div");

    mensaje.classList.add("mensaje");

    if(tipo === "usuario"){
        mensaje.classList.add("usuario");
    }

    mensaje.innerHTML =
    `
        ${tipo === "bot"
            ? '<div class="avatar-bot"></div>'
            : ''}

        <div class="burbuja">
            ${texto}
        </div>
    `;

    mensajes.appendChild(mensaje);

    mensajes.scrollTop = mensajes.scrollHeight;
}

async function enviarMensaje(){

    const texto = input.value.trim();

    if(texto === ""){
        return;
    }

    agregarMensaje(texto,"usuario");

    input.value = "";

    try{

        const respuesta = await fetch("/mensaje",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                mensaje:texto
            })
        });

        const datos = await respuesta.json();

        agregarMensaje(datos.respuesta,"bot");

    }
    catch(error){

        agregarMensaje(
            "Error al conectar con el servidor.",
            "bot"
        );
    }
}

boton.addEventListener("click",enviarMensaje);

input.addEventListener("keydown",(e)=>{

    if(e.key === "Enter"){
        enviarMensaje();
    }

});
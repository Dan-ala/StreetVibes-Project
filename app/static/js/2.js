//Reglas de validacion


let flag
const number=/^[0-9]{2,15}$/
const text=/[a-zA-Zá-úÁ-Ú ]{10,50}/
//acceder a los elemetos del form
const form=document.getElementById("formularioCate")


//Ingresar al formulario y busca por el nombre 
const nom=form.categoria.value

//acceder al ficback
result=document.querySelector("#categoria .feedback")


//Otra forma de acceder al valor 

form.nom.addEventListener('input',(e)=>{
e.preventDefault()
 alert("Se esta escriendo sobre el input")
if(number.test(e.target.value)){
    form.nom.setAttribute("class","success")
    alert("hola")
    result.style.setProperty("visibility","hidden")
    result.style.setProperty("opacity","0")
    flag=true


}
else{
    form.nom.setAttribute("class","error")
    result.textContent="SOlo digite bien "
    result.style.setProperty("visibility","visible")
    result.style.setProperty("opacity","1")
    flag=false
    
}
})




/
    form.addEventListener("submit",e=>{
        e.preventDefault()
    
        if(form.nom.value==null || form.nom.value==0 ||flag2==false){
            alert("Ingrese un Nombre valido")
            form.nom.focus()
            form.nom.setAttribute("class","error")}

    
        else{
            form.submit()
        }
    })




x=document.getElementsByClassName("removeItemCart")
let row=document.createElement("div")
row.classList.add("row","mb-3")
let col=document.createElement("div")
col.classList.add("col-lg-12")
let p=document.createElement("p")
p.classList.add("note","note-light")

let strong=document.createElement("strong")
strong.textContent="Nota:"
p.appendChild(strong)
let txt="Aún no ha agregado productos a su carrito"
strong.after(txt)
col.appendChild(p)
row.appendChild(col)
if (document.getElementById("btnCheck")!=null) {
    

document.getElementById("btnCheck").addEventListener("click",function(){
      
            var login = $.confirm({
                title: "",
                columnClass: "col-lg-5 col-md-7 col-xs-9",
                closeIcon: true,
                content: function () {
                  var self = this;
                  return $.ajax({
                      url: "/login",
                      dataType: "json",
                    })
                    .done(function (response) {
                      self.setContent(response.html);
                    })
                },
                buttons: {
                  okButton: {
                    text: "ok",
                    action: function () {},
                  },
                },               
                onContentReady: function (e) {
                  this.buttons.okButton.hide();            
                },                        
              });
     
 
})}
for (let i = 0; i < x.length; i++) {
    const element = x[i];
    element.addEventListener("click",function () {
       let pinpt=element.closest(".groupInput").firstChild.nextSibling.id
       let converted=parseInt(pinpt.split("_").pop())
       let data={converted}
    
    //    <div class="row">
    //    <div class="col-lg-12"><p class="note note-light">
    //        <strong>Nota:</strong> Aún no ha agregado productos a su carrito
    //      </p></div>print
    //     </div>
       fetch(this.dataset.url,{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        },body:  JSON.stringify(data)}).then(data=>data.json()).then(response=>{
            console.log(response);
            if(response.status!=0){
            document.getElementById("cartCount").innerHTML=response.quantity-response.count
            document.getElementById("abstractContent").innerHTML=`Subtotal (${response.quantity-response.count} productos) :`
            document.getElementById("abstractTotalCart").innerHTML=`S/. ${response.total}`
            document.getElementById("abstract_TotalCart").innerHTML=`S/. ${response.total}`

            }else{
                document.getElementById("cartCount").innerHTML=response.quantity
                document.getElementById("abstractContent").innerHTML=`Subtotal (${response.quantity} productos) :`
                document.getElementById("abstractTotalCart").innerHTML=`S/. ${response.total}`
                document.getElementById("abstract_TotalCart").innerHTML=`S/. ${response.total}`

            }
            element.closest(".cartItem").style.animationPlayState="running"
            element.closest(".cartItem").addEventListener("animationend",()=>{
                element.closest(".cartItem").remove()
            })
            
            
            if (document.getElementsByClassName("cartItem").length==1) {
                document.getElementById("col-price").remove()

                document.getElementById("idContentCart").appendChild(row)

            }
        
        })
      })
}
const selectElementAuth = document.getElementsByClassName('SelectCartCountAuth');


Array.from(selectElementAuth).forEach(element=>{
    element.addEventListener("change",(e)=>{
        let newCount=e.target.value
        let pinpt=element.closest(".groupInput").firstChild.nextSibling.id
        let converted=parseInt(pinpt.split("_").pop())
        let data={converted,newCount}
        let url=e.target.dataset.url
        fetch(url,{
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken
            },body:  JSON.stringify(data)})
            .then(data=>data.json())
            .then(response=>{
                document.getElementById("cartCount").innerHTML=response.quantity
                document.getElementById("abstractContent").innerHTML=`Subtotal (${response.quantity} productos) :`
                document.getElementById("abstractTotalCart").innerHTML=`S/. ${response.total}`
                document.getElementById("abstract_TotalCart").innerHTML=`S/. ${response.total}`
                if (newCount==0) {
                    element.closest(".cartItem").style.animationPlayState="running"

                    element.closest(".cartItem").addEventListener("animationend",()=>{
                        element.closest(".cartItem").remove()
                    })
                    
                    console.log(document.getElementsByClassName("cartItem").length)
                    if (document.getElementsByClassName("cartItem").length==1) {
                        document.getElementById("col-price").remove()
                        document.getElementById("idContentCart").appendChild(row)
                        
                    }
                }
            })
        
           

    })
    
})
let adresscomponent=document.getElementsByClassName("address-orders")
Array.from(adresscomponent).forEach(element=>{
    console.log(element.className);
    element.addEventListener("click",(e)=>{
        Array.from(adresscomponent).forEach(element2=>{
                element2.classList.add("active-adress")
                if(element2.childNodes[2].nextSibling.childNodes[2]!=undefined){
                    element2.childNodes[2].nextSibling.removeChild(element2.childNodes[2].nextSibling.childNodes[2])

                }    
       
        })
        e.target.classList.remove("active-adress")
        let valdir=e.target.childNodes[2].nextElementSibling.className;
        document.getElementById("address").value=parseInt(valdir.split("_").pop())
        let img=document.createElement("img")
        img.src="/static/icons/comprobado.png"
        e.target.childNodes[2].nextElementSibling.appendChild(img)


    })
})
function next_step() { 
    document.getElementById("tab-2").disabled=false

    document.getElementById("tab-2").click()
 }
 function next_step_3() { 
     if ( !document.getElementById("address").value=="") {
        document.getElementById("tab-3").disabled=false

        document.getElementById("tab-3").click()
     }
     else{
        alert("Seleccione una dirección");
     }
 }
function seeformAdress() 
{  
    document.getElementById("add_adress_circle").classList.add("none")
    document.querySelector(".form_Address").classList.remove("none")
}
function cancelAddress(){
    document.getElementById("add_adress_circle").classList.remove("none")
    document.querySelector(".form_Address").classList.add("none")
}
const fetch_edit_account=(data,url)=>{
    fetch(url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
           "X-CSRFToken":csrftoken
        },
        body:JSON.stringify(data)
    }).then(data=>data.json()).then(response=>console.log(response))
}
function editData(){
     document.getElementById("order_input_name").disabled=false
    document.getElementById("order_input_last").disabled=false
    document.getElementById("btn_edit_order").removeAttribute("onclick")
    document.getElementById("btn_edit_order").innerHTML="Guardar"
    let url=document.getElementById("btn_edit_order").dataset.url
    document.getElementById("btn_edit_order").setAttribute("onclick",`save_data(${url})`)
    document.getElementById("btn_next_step2").disabled=true
}
function save_data(url){
    let name=document.getElementById("order_input_name").value
    let last=document.getElementById("order_input_last").value

    document.getElementById("btn_next_step2").disabled=false
    document.getElementById("btn_edit_order").removeAttribute("onclick")
    document.getElementById("btn_edit_order").innerHTML="Editar"
    document.getElementById("btn_edit_order").setAttribute("onclick","editData()")
    document.getElementById("order_input_name").disabled=true
    document.getElementById("order_input_last").disabled=true
    let data={name,last}
    fetch_edit_account(data,url)
    

}

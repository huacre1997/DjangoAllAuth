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
            document.getElementById("cartCount").innerHTML=response.quantity-response.count
            document.getElementById("abstractContent").innerHTML=`Subtotal (${response.quantity-response.count} productos) :`
            document.getElementById("abstractTotalCart").innerHTML=`S/. ${response.total}`
            element.closest(".cartItem").style.animationPlayState="running"
            element.closest(".cartItem").addEventListener("animationend",()=>{
                element.closest(".cartItem").remove()
            })
            
            
            if (document.getElementsByClassName("cartItem").length==1) {
                document.getElementById("idContentCart").appendChild(row)

            }
        })
      })
}
const selectElement = document.getElementsByClassName('SelectCartCount');

Array.from(selectElement).forEach(element=>{
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
                if (newCount==0) {
                    element.closest(".cartItem").style.animationPlayState="running"

                    element.closest(".cartItem").addEventListener("animationend",()=>{
                        element.closest(".cartItem").remove()
                    })
                    
                    console.log(document.getElementsByClassName("cartItem").length)
                    if (document.getElementsByClassName("cartItem").length==1) {
                        document.getElementById("idContentCart").appendChild(row)
        
                    }
                }
            })
        
           

    })
    
})
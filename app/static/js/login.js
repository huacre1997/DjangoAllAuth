

$(function () {
    $("#logout").on("click", function () {
        url=$(this).attr("to")
        location.href=url
    });
    $("#btnLogin").on("click",function(){
        console.log("Entro al event");
         url=$(this).attr("hreft")
           
        $.confirm({
                    title:"",
                    columnClass: 'col-lg-5 col-md-7 col-xs-9',
                    closeIcon: true,
                    content: function () {
                        var self = this;
                        return $.ajax({
                            url: url,
                            dataType: 'json',
                            method: 'get'
                        }).done(function (response) {
                            self.setContent(response.html);
                         
                        }).fail(function(){
                            self.setContent('Something went wrong.');
                        });
                    },
                    buttons: {
                        okButton: {
                             text: 'ok',
                             action: function () {
                             }
                         }
                     },
                     onContentReady: function () {
                         // when content is fetched & rendered in DOM
                 
                            this.buttons.okButton.hide();
                          
                     },
                  
                });
    

        });
    
});
const ajaxfunc=(url)=>{

}
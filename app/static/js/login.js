
$(function () {
    $("#logout").on("click", function () {
        url=$(this).attr("to")
        location.href=url
    });
    $("#btnLogin").on("click",function(){

        $("#navbarSupportedContent").removeClass("show")
         url=$(this).attr("hreft")
           console.log(url);
         const login=$.confirm({
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
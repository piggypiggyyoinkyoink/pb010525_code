<script>
    let {id, text="Submit"} = $props();
</script>
<div>
    <input type = "submit" class = "svc_SubmitButton" value = {text}>
</div>
<style>
    input{
        background-color:rgb(10, 179, 4);
        font-size:18px;
        padding:5px;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin:5px;
        border-radius:10px;
        border:3px solid black;
        cursor:pointer;
    }
    div{
        text-align:center;
    }
</style>
<script>
    let {id, type="text", name=id, placeholder="", label=null} = $props();
</script>
{#if label}
<label for = {id}>{label}:</label><br>
{/if}
<input type = {type} id = {id} name = {name} placeholder = {placeholder}><br>

<style>
    input{
        font-size:18px;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-radius:8px;
        border:3px solid black;
        padding:5px;
        margin:auto;
    }
    label{
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size:18px;
    }
</style>
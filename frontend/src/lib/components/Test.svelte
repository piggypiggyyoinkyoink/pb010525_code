<script>
    import { onMount } from "svelte";
    let msg = $state()

    onMount(async() =>{
        try{
            
            let data = await fetch("http://localhost:8000/")
            let dataJson = await data.json()
            console.log(dataJson.message)
            msg = dataJson.message
        }catch(e){
            console.log(e)
            msg = "p"
        }
    })
</script>

<div>
    <p> {msg}</p>
</div>
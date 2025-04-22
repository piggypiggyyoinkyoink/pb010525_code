<script>
    import FormField from "./FormField.svelte";
    import SubmitButton from "./SubmitButton.svelte";
    let valid = $state(true)
    let {id="loginForm", action} = $props()
    async function submit(event,url=action){
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch("http://localhost:8000/token", {
            method:"POST",
            body: formData
        })
        let data = await response.json()
        if (response.ok){
            window.location.replace(`http://localhost:5173/home/?token=${data.access_token}`)
        }else{
            valid = false
        }

    }
</script>

<div>
    <form id = {id} class = "loginForm" onsubmit={submit} method = "post">
        <FormField id = "username" type = "text" placeholder = "Enter username..." label = "Username"></FormField>
        <FormField id = "password" type = "password" placeholder = "Enter password..." label = "Password"></FormField>
        <SubmitButton></SubmitButton>
    </form>
    {#if !valid}
    <p>Invalid username and password</p>
    {/if}
</div>

<style>
    form{
        margin:auto;
        width:fit-content;
    }
    p{
        color:red;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size:18px;
        text-align:center;
    }
</style>
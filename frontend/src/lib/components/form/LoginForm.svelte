<script>
    import FormField from "./FormField.svelte";
    import SubmitButton from "./SubmitButton.svelte";

    let {id="loginForm", action} = $props()
    async function submit(event,url=action){
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch("http://localhost:8000/token", {
            method:"POST",
            body: formData
        })
        console.log(await response.json());
        console.log(await response.status);

    }
</script>

<div>
    <form id = {id} class = "loginForm" onsubmit={submit} method = "post">
        <FormField id = "username" type = "text" placeholder = "Enter username..." label = "Username"></FormField>
        <FormField id = "password" type = "password" placeholder = "Enter password..." label = "Password"></FormField>
        <SubmitButton></SubmitButton>
    </form>
</div>

<style>
    form{
        margin:auto;
        width:fit-content;
    }
</style>
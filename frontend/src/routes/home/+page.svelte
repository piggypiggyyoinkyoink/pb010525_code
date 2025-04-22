<script>
    import {browser} from "$app/environment";
    let data = $state(null)
    if (browser){
        async function getData(){
            const searchParams = new URLSearchParams(window.location.search);
            const token = searchParams.get("token");
            console.log(token);
            if (!(!token)){
                try{
                    let fetchData = await fetch("http://localhost:8000/users/me",{
                        headers:{
                            "Authorization": "Bearer " +token
                        }
                    });
                    if (!fetchData.ok){
                        window.location.replace("http://localhost:5173/login");

                    }
                    data = await fetchData.json()
                    console.log(data);
                }catch{
                    window.location.replace("http://localhost:5173/login");

                }
                
            }else{
                window.location.replace("http://localhost:5173/login");
    
            }
                
        }

        getData();
    }
</script>

<p>Hello{#if data}, {data.first_name}{/if}</p>
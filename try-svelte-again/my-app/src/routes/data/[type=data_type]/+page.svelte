<!--THIS IS THE /data/[type] PAGE-->
<script>
    import { page } from '$app/stores';

    let type = 'null';
    type = String($page.url.pathname).split('/')[2];
</script>


<h1>This is the data page for type: {type}</h1>
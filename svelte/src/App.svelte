<script>
	import Chat from './Scheduler.svelte';
	import BouncingDots from './BouncingDots.svelte'  
</script>

<main>
	<Chat />
</main> 

<style>
	:global(body) {
		background: #000;
	}
	
	main {
		width: 500px;
		margin: 50px auto;
	} 
</style>
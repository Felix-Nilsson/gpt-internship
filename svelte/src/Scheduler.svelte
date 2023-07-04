<script>
	import { onMount } from 'svelte';
	import ChatBox from './ChatBox.svelte';
	
	
	let transformed_data = []
	export let data = [{
		text: 'Hi!',
		who: 'them',
	}, {
		text: 'Let\'s discover a little more about you!', 
		who: 'them',
	}, {
		text: 'When exploring opportunities and starting new projects, you...',
		who: 'them',
	},{
		text: 'Hi!',
		who: 'you',
	}, {
		text: 'Let\'s discover a little more about you!', 
		who: 'them',
	}, {
		text: 'When exploring opportunities and starting new projects, you...',
		who: 'them',
	},{
		text: 'Hi!',
		who: 'them',
	}, {
		text: 'Let\'s discover a little more about you!', 
		who: 'them',
	}, {
		text: 'When exploring opportunities and starting new projects, you...',
		who: 'them',
	},{
		text: 'Hi!',
		who: 'you',
	}, {
		text: 'Let\'s discover a little more about you!', 
		who: 'them',
	}, {
		text: 'When exploring opportunities and starting new projects, you...',
		who: 'them',
	}];
	
	let current = [];
	let timer = 0;
	let current_index = 0; 
	
	function readingTime(text) {
		const wps = (225 / 60);
		const words = text.trim().split(/\s+/).length;
		const time = Math.ceil((words / wps) * 1000);
		return time;
	}
	
	let accumulated_time = 0;
	for (let i = 0; i < data.length; i++) { 
		const time = readingTime(data[i].text);
		const _data = {
			...data[i],
			ready: false,
			isolateDelay: time,
			delay: accumulated_time + (time < 1500 ? 1500 : time * 2),
			final: i === data.length-1
		}
		accumulated_time = _data.delay
		transformed_data.push(_data)
	}	
	
	
	function run() {
			const elapsed = performance.now() - timer;
			if (elapsed > transformed_data[current_index].delay) {
					transformed_data[current_index].ready= true;
					current = current;
					if (!transformed_data[current_index+1]) return;
					transformed_data[current_index+1] && current_index++;

					current.push(transformed_data[current_index]); 
				  current = current;
					   
			}  
		
			requestAnimationFrame(run)   
	}
	
	function schedule() { 
		timer = performance.now()
		requestAnimationFrame(run) 
	}
	
	onMount(() => {
		current.push(transformed_data[current_index]);
		current = current;
		schedule(); 
	})
	
</script>

<div>
	{#each current as {text, who, ready, final, isolateDelay} }
		<ChatBox {who} {text} {ready} {final} {isolateDelay}/>
	{/each}
</div>

<style>
	div {

	padding-bottom: 50px
	}
</style>
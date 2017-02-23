<template>
	<div class="list">
		<div class="left-wrapper">
		<ul>
			<li :id="index" v-bind:class="{active: index==currentUserId}" v-on:click="showUser($event, index)" v-for="hren,index in userData">
				User #{{index+1}}
			</li>
		</ul>
		</div>
		<div class="right-wrapper">
			<h2 align="center">{{this.currentUser.name}} {{this.currentUser.lastname}}</h2>

			<div class="flex">
				<user-chart title="Release-to-Release time" param="r2r" :chartData="this.currentUser"></user-chart>
				<user-chart title="Press-to-Press time" param="p2p" :chartData="this.currentUser"></user-chart>
				<user-chart title="Flight Time" param="flight" :chartData="this.currentUser"></user-chart>
				<user-chart title="Dwell time" param="dwell" :chartData="this.currentUser"></user-chart>
				<user-chart title="Mouse speed" param="ms" :chartData="this.currentUser"></user-chart>
				<user-chart title="Double click speed" param="dbcs" :chartData="this.currentUser"></user-chart>
				<user-chart title="Left click speed" param="lcs" :chartData="this.currentUser"></user-chart>
				<user-chart title="Right click speed" param="rcs" :chartData="this.currentUser"></user-chart>
			</div>
		</div>

	</div>
</template>

<script>
	import Behave from  "../behave-lib.js"
	import ChartLine from "../Collect-Demo/charts/line.vue"
	import UserChart from "./userChart.vue"
	export default {

		components : {ChartLine, UserChart},
		data() {
			return {
				userData: {},
				currentUserId: 0,
				currentUser: {},
			};
		},

		beforeMount(){
			this.requestUsersData();
		},



		methods : {
			showUser($event, id) {
				this.currentUser=  this.userData[id];
				this.currentUserId = id;
			},
			requestUsersData() {
				let data = this.userData;
				let requestUrl = "http://127.0.0.1:5000/users";
				let successCallback = (response) => {
					this.userData = response.data;
					this.currentUser = this.userData[0];
				}


				let errorCallback = (response) => {
					console.error(response);
				}

				this.$http.get(requestUrl).then(successCallback, errorCallback)
			}
		}

	}
</script>

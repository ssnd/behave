export default {
	get_auth() {
		var token = localStorage.getItem("auth_token");
		return token ? token : false
	},

	get_auth_header() {
		return {
			"Authorization" : this.get_auth()
		}
	},

	set_auth(token) {
		localStorage.setItem("auth_token", token)
		localStorage.setItem("logged_in", 1)
	}
}
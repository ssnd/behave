export default {	
	get_auth() {
		var token = localStorage.getItem("auth_token")
		return token ? token : false
	},

	get_auth_header() {
		return {
			"Authorization" : this.get_auth()
		}
	},

	set_auth(token, user) {
		localStorage.setItem("auth_token", token)
		localStorage.setItem("logged_in", 1)
		localStorage.setItem("logged_user", user)
	},

	set_logout() {
		localStorage.setItem("auth_token", null)
		localStorage.setItem("logged_in", 0)
		localStorage.setItem("logged_user", "")
	}
}
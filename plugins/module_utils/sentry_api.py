#!/usr/bin/python

import requests
import json


class SentryApi(object):
	CREATE_PROJECT_URL = "/api/0/teams/{organization_slug}/{team_slug}/projects/"
	RETRIEVE_PROJECT_URL = "/api/0/projects/{organization_slug}/{project_slug}/"
	UPDATE_PROJECT_URL = "/api/0/projects/{organization_slug}/{project_slug}/"
	DELETE_PROJECT_URL = "/api/0/projects/{organization_slug}/{project_slug}/"

	CREATE_TEAM_URL = "/api/0/organizations/{organization_slug}/teams/"
	RETRIEVE_TEAM_URL = "/api/0/teams/{organization_slug}/{team_slug}/"
	UPDATE_TEAM_URL = "/api/0/teams/{organization_slug}/{team_slug}/"
	DELETE_TEAM_URL = "/api/0/teams/{organization_slug}/{team_slug}/"

	RETRIEVE_ORGANIZATION_URL = "/api/0/organizations/{organization_slug}/"
	UPDATE_ORGANIZATION_URL = "/api/0/organizations/{organization_slug}/"

	CREATE_CLIENT_KEY_URL = "/api/0/projects/{organization_slug}/{project_slug}/keys/"
	UPDATE_CLIENT_KEY_URL = "/api/0/projects/{organization_slug}/{project_slug}/keys/{client_key}/"
	DELETE_CLIENT_KEY_URL = "/api/0/projects/{organization_slug}/{project_slug}/keys/{client_key}/"

	CREATE_SERVICE_HOOK_URL = "/api/0/projects/{organization_slug}/{project_slug}/hooks/"
	UPDATE_SERVICE_HOOK_URL = "/api/0/projects/{organization_slug}/{project_slug}/hooks/{hook_id}/"
	DELETE_SERVICE_HOOK_URL = "/api/0/projects/{organization_slug}/{project_slug}/hooks/{hook_id}/"

	def __init__(self, module, host, token):
		self.module = module
		self.host = host

		self.headers = {
			'Authorization': 'Bearer '+token, 
			'Content-Type': 'application/json'
		}

		self.result = dict(
			message=''
		)

	def build_url(self, url):
		return self.host+url

	def get_url(self, task):
		if task == 'create-project':
			return self.build_url(self.CREATE_PROJECT_URL.format(
						organization_slug=self.organization_slug,
						team_slug=self.team_slug
					))
		elif task == 'retrieve-project':
			return self.build_url(self.RETRIEVE_PROJECT_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug
					))
		elif task == 'update-project':
			return self.build_url(self.UPDATE_PROJECT_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug
					))
		elif task == 'delete-project':
			return self.build_url(self.DELETE_PROJECT_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug
					))
		elif task == 'create-team':
			return self.build_url(self.CREATE_TEAM_URL.format(
						organization_slug=self.organization_slug
					))
		elif task == 'retrieve-team':
			return self.build_url(self.RETRIEVE_TEAM_URL.format(
						organization_slug=self.organization_slug,
						team_slug=self.team_slug
					))
		elif task == 'update-team':
			return self.build_url(self.UPDATE_TEAM_URL.format(
						organization_slug=self.organization_slug,
						team_slug=self.team_slug
					))
		elif task == 'delete-team':
			return self.build_url(self.DELETE_TEAM_URL.format(
						organization_slug=self.organization_slug,
						team_slug=self.team_slug
					))
		elif task == 'retrieve-organization':
			return self.build_url(self.RETRIEVE_ORGANIZATION_URL.format(
						organization_slug=self.organization_slug
					))
		elif task == 'update-organization':
			return self.build_url(self.UPDATE_ORGANIZATION_URL.format(
						organization_slug=self.organization_slug
					))
		elif task == 'create-client-key':
			return self.build_url(self.CREATE_CLIENT_KEY_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug
					))
		elif task == 'update-client-key':
			return self.build_url(self.UPDATE_CLIENT_KEY_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug,
						client_key=self.client_key
					))
		elif task == 'delete-client-key':
			return self.build_url(self.DELETE_CLIENT_KEY_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug,
						client_key=self.client_key
					))
		elif task == 'create-service-hook':
			return self.build_url(self.CREATE_SERVICE_HOOK_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug
					))
		elif task == 'update-service-hook':
			return self.build_url(self.UPDATE_SERVICE_HOOK_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug,
						hook_id=self.hook_id
					))
		elif task == 'delete-service-hook':
			return self.build_url(self.DELETE_SERVICE_HOOK_URL.format(
						organization_slug=self.organization_slug,
						project_slug=self.project_slug,
						hook_id=self.hook_id
					))

	def create_project(self, organization_slug, team_slug, name, slug):
		self.organization_slug = organization_slug
		self.team_slug = team_slug
		result = self.result

		payload = {
	        'name': name,
	        'slug': slug
	    }

		create_project_url = self.get_url('create-project')

		create_requests = requests.post(create_project_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = create_project_url
		result['status_code'] = create_requests.status_code
		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project has been created"

		if create_requests.status_code != 201:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't create project"

		result['response'] = create_requests.json()

		return result

	def retrieve_project(self, organization_slug, project_slug):
		self.organization_slug = organization_slug
		self.project_slug = project_slug

		result = self.result

		retrieve_project_url = self.get_url('retrieve-project')

		retrieve_requests = requests.get(retrieve_project_url, headers=self.headers)

		result['url'] = retrieve_project_url
		result['status_code'] = retrieve_requests.status_code
		result['changed'] = False
		result['failed'] = False
		result['message'] = "Project is available"

		if retrieve_requests.status_code != 200:
			result['failed'] = True
			result['message'] = "Can't retrieve project"

		result['response'] = retrieve_requests.json()

		return result

	def update_project(self, organization_slug, project_slug, team_slug, name, slug, platform, is_bookmarked):
		self.organization_slug = organization_slug
		self.project_slug = project_slug

		result = self.result

		payload = {
		    'name': name,
		    'slug': slug,
		    'team_slug': team_slug,
		    'platform': platform,
		    'is_bookmarked': is_bookmarked
		}

		update_project_url = self.get_url('update-project')

		update_requests = requests.put(update_project_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = update_project_url
		result['status_code'] = update_requests.status_code
		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project has been updated"
		
		if update_requests.status_code != 200:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't update orihect"

		result['response'] = update_requests.json()

		return result

	def delete_project(self, organization_slug, project_slug):
		self.organization_slug = organization_slug
		self.project_slug = project_slug
		result = self.result

		delete_project_url = self.get_url('delete-project')

		delete_requests = requests.delete(delete_project_url, headers=self.headers)

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project has been deleted"
		result['response'] = {
			"detail": "Success"
		}

		if delete_requests.status_code != 204:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't delete project"
			result['response'] = delete_requests.json()

		return result

	def create_team(self, organization_slug, name, slug):
		self.organization_slug = organization_slug
		result = self.result

		payload = {
	        'name': name,
	        'slug': slug
	    }

		create_team_url = self.get_url('create-team')

		create_requests = requests.post(create_team_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = create_team_url
		result['status_code'] = create_requests.status_code

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Team has been created"
		
		if create_requests.status_code != 201:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't create team"

		result['response'] = create_requests.json()
		
		return result

	def retrieve_team(self, organization_slug, team_slug):
		self.organization_slug = organization_slug
		self.team_slug = team_slug

		result = self.result

		retrieve_team_url = self.get_url('retrieve-team')

		retrieve_requests = requests.get(retrieve_team_url, headers=self.headers)

		result['url'] = retrieve_team_url
		result['status_code'] = retrieve_requests.status_code
		
		result['changed'] = False
		result['failed'] = False
		result['message'] = "Team is available"
		
		if retrieve_requests.status_code != 200:
			result['failed'] = True
			result['message'] = "Can't retrieve team"

		result['response'] = retrieve_requests.json()

		return result

	def update_team(self, organization_slug, team_slug, name, slug):
		self.organization_slug = organization_slug
		self.team_slug = team_slug

		result = self.result

		payload = {
		    'name': name,
		    'slug': slug
		}

		update_team_url = self.get_url('update-team')

		update_requests = requests.put(update_team_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = update_team_url
		result['status_code'] = update_requests.status_code

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Team has been updated"

		if update_requests.status_code != 200:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't update team"

		result['response'] = update_requests.json()

		return result

	def delete_team(self, organization_slug, team_slug):
		self.organization_slug = organization_slug
		self.team_slug = team_slug
		result = self.result

		delete_team_url = self.get_url('delete-team')

		delete_requests = requests.delete(delete_team_url, headers=self.headers)

		result['url'] = delete_team_url
		result['status_code'] = delete_requests.status_code

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Team has been deleted"
		result['response'] = {
			"detail": "Success"
		}

		if delete_requests.status_code != 204:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't delete team"
			result['response'] = delete_requests.json()

		return result

	def retrieve_organization(self, organization_slug):
		self.organization_slug = organization_slug

		result = self.result

		retrieve_organization_url = self.get_url('retrieve-organization')

		retrieve_requests = requests.get(retrieve_organization_url, headers=self.headers)

		result['url'] = retrieve_organization_url
		result['status_code'] = retrieve_requests.status_code

		result['changed'] = False
		result['failed'] = False
		result['message'] = "Organization is available"

		if retrieve_requests.status_code != 200:
			result['failed'] = True
			result['message'] = "Can't retrieve the organization"

		result['response'] = retrieve_requests.json()

		return result

	def update_organization(self, organization_slug, name, slug):
		self.organization_slug = organization_slug

		result = self.result

		payload = {
		    'name': name,
		    'slug': slug
		}

		update_organization_url = self.get_url('update-organization')

		update_requests = requests.put(update_organization_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = update_organization_url
		result['status_code'] = update_requests.status_code

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Organization has been updated"

		if update_requests.status_code != 200:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't update organization"

		result['response'] = update_requests.json()

		return result

	def create_client_key(self, organization_slug, project_slug, name):
		self.organization_slug = organization_slug
		self.project_slug = project_slug
		result = self.result

		payload = {
	        'name': name
	    }

		create_client_key_url = self.get_url('create-client-key')

		create_requests = requests.post(create_client_key_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = create_client_key_url
		result['status_code'] = create_requests.status_code
		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project Client Key has been created"

		if create_requests.status_code != 201:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't create client key"

		result['response'] = create_requests.json()

		return result

	def update_client_key(self, organization_slug, project_slug, client_key, name, is_active):
		self.organization_slug = organization_slug
		self.project_slug = project_slug
		self.client_key = client_key

		result = self.result

		payload = {
		   'name': name,
		   'isActive': is_active
		}

		update_client_key_url = self.get_url('update-client-key')

		update_requests = requests.put(update_client_key_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = update_client_key_url
		result['status_code'] = update_requests.status_code
		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project Client Key has been updated"

		if update_requests.status_code != 200:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't update client key"

		result['response'] = update_requests.json()

		return result

	def delete_client_key(self, organization_slug, project_slug, client_key):
		self.organization_slug = organization_slug
		self.project_slug = project_slug
		self.client_key = client_key

		result = self.result

		delete_client_key_url = self.get_url('delete-client-key')

		delete_requests = requests.delete(delete_client_key_url, headers=self.headers)

		result['url'] = delete_client_key_url
		result['status_code'] = delete_requests.status_code

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project Client Key has been deleted"
		result['response'] = {
			"detail": "Success"
		}

		if delete_requests.status_code != 204:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't delete client key"
			result['response'] = delete_requests.json()

		return result

	def create_service_hook(self, organization_slug, project_slug, hook_url, hook_events):
		self.organization_slug = organization_slug
		self.project_slug = project_slug

		result = self.result

		payload = {
	        'url': hook_url,
	        'events': hook_events
	    }

		create_service_hook_url = self.get_url('create-service-hook')

		create_requests = requests.post(create_service_hook_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = create_service_hook_url
		result['status_code'] = create_requests.status_code
		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project Service Hook has been created"

		if create_requests.status_code != 201:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't create service hook"

		result['response'] = create_requests.json()
		
		return result

	def update_service_hook(self, organization_slug, project_slug, hook_id, hook_url, hook_events):
		self.organization_slug = organization_slug
		self.project_slug = project_slug
		self.hook_id = hook_id

		result = self.result

		payload = {
	        'url': hook_url,
	        'events': hook_events
	    }

		update_service_hook_url = self.get_url('update-service-hook')

		update_requests = requests.put(update_service_hook_url, data=json.dumps(payload), headers=self.headers)

		result['url'] = update_service_hook_url
		result['status_code'] = update_requests.status_code
		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project Service Hook has been updated"

		if update_requests.status_code != 200:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't update service hook"

		result['response'] = update_requests.json()

		return result

	def delete_service_hook(self, organization_slug, project_slug, hook_id):
		self.organization_slug = organization_slug
		self.project_slug = project_slug
		self.hook_id = hook_id

		result = self.result

		delete_service_hook_url = self.get_url('delete-service-hook')

		delete_requests = requests.delete(delete_service_hook_url, headers=self.headers)

		result['url'] = delete_service_hook_url
		result['status_code'] = delete_requests.status_code

		result['changed'] = True
		result['failed'] = False
		result['message'] = "Project Service Hook has been deleted"
		result['response'] = {
			"detail": "Success"
		}

		if delete_requests.status_code != 204:
			result['changed'] = False
			result['failed'] = True
			result['message'] = "Can't delete service hook"
			result['response'] = delete_requests.json()

		return result

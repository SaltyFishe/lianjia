import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/login',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    url: '/api/register',
    method: 'post',
    data
  })
}

export function modify(data) {
  return request({
    url: '/api/modify',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/api/user/info',
    method: 'get'
    // params: { token }
  })
}

export function logout() {
  return request({
    url: '/api/logout',
    method: 'post'
  })
}

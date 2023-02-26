import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/vue-admin-template/table/list',
    method: 'get',
    params
  })
}

export function getGeneralData() {
  return request({
    url: '/api/statistics/general',
    method: 'get'
  })
}

export function getAreaData() {
  return request({
    url: '/api/statistics/area',
    method: 'get'
  })
}

export function getCommunityData() {
  return request({
    url: '/api/statistics/community',
    method: 'get'
  })
}


export function getPriceData() {
  return request({
    url: '/api/statistics/price',
    method: 'get'
  })
}


export function getDecorateData() {
  return request({
    url: '/api/statistics/decorate',
    method: 'get'
  })
}

export function getCityData(param) {
  return request({
    url: '/api/statistics/city?name=' + param,
    method: 'get'
  })
}

export function getSizePriceData() {
  return request({
    url: '/api/statistics/size_price',
    method: 'get'
  })
}


export function startCrawler() {
  return request({
    url: '/api/crawler',
    method: 'post'
  })
}

export function stopCrawler() {
  return request({
    url: '/api/crawler',
    method: 'patch'
  })
}

export function getCrawlerLog() {
  return request({
    url: '/api/crawler',
    method: 'get'
  })
}

export function predict(data) {
  return request({
    url: '/api/predict',
    method: 'post',
    data
  })
}

export function updatePredictResult() {
  return request({
    url: '/api/predict',
    method: 'put'
  })
}

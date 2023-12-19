import {request} from "../utils/requests";

export function getRules() {
    return request.request({
        url: '/rule/',
        method: 'get'
    })
}


export function modifyRule(data: any) {
    return request.request({
        url: '/rule/',
        method: data.id ? 'put' : 'post',
        data: data
    })
}


export function triggerRule(rule_id: number) {
    return request.request({
        url: '/rule/trigger',
        method: 'post',
        params: {rule_id}
    })
}

export function getHistories(rule_id: number, only_update: boolean) {
    return request.request({
        url: '/rule/history',
        method: 'get',
        params: {rule_id, only_update}
    })
}

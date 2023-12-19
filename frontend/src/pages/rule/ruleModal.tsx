import {Col, Form, Input, Modal, Row, Select, Switch} from "antd";
import {FormModalProps} from "../../utils/useFormModal";
import React from "react";
import {VerticalRightOutlined} from "@ant-design/icons";
import * as api from "../../apis/notify";
import {useRequest} from "ahooks";
import {NotifyItem} from "../notify/item";
import {notifies} from "../../utils/constants";


function RuleModal(props: FormModalProps) {
    const {form, initValues, ...otherProps} = props

    const {
        data: notifyOptions = [],
        loading: loadingNotifies
    } = useRequest(async () => (await api.getNotifies()).data.data)

    const id = initValues?.id

    return (
        <Modal title={id ? '编辑规则' : '新建规则'} width={680} {...otherProps}>
            <Form form={form} layout={'vertical'}>
                <Row gutter={20}>
                    <Col span={24} lg={12}>
                        <Form.Item name={'name'} label={'名称'} rules={[{required: true, message: '请输入名称'}]}>
                            <Input/>
                        </Form.Item>
                    </Col>
                    <Col span={24} lg={12}>
                        <Form.Item name={'cron'} label={'Crontab'}
                                   rules={[{required: true, message: '请输入Crontab表达式'}]}>
                            <Input/>
                        </Form.Item>
                    </Col>
                </Row>
                <Form.Item name={'url'} label={'URL'} rules={[{required: true, message: '请输入URL'}]}>
                    <Input/>
                </Form.Item>
                <Form.Item name={'user_agent'} label={'User-Agent'}>
                    <Input addonAfter={(<VerticalRightOutlined
                        onClick={() => form?.setFieldValue('user_agent', window.navigator.userAgent)}
                        style={{cursor: 'pointer'}}/>)}/>
                </Form.Item>
                <Form.Item name={'cookies'} label={'Cookies'}>
                    <Input.TextArea/>
                </Form.Item>
                <Form.Item name={'notify_ids'} label={'通知'}>
                    <Select loading={loadingNotifies} mode={"multiple"}>
                        {notifyOptions.map((item: any) => (
                            <Select.Option key={item.id} value={item.id}>
                                <NotifyItem size={15} name={item.name} icon={notifies[item.type].icon}/>
                            </Select.Option>
                        ))}
                    </Select>
                </Form.Item>
                <Row gutter={20}>
                    <Col span={24} lg={12}>
                        <Form.Item name={'xpath'} label={'XPath表达式'}>
                            <Input/>
                        </Form.Item>
                    </Col>
                    <Col span={24} lg={12}>
                        <Form.Item name={'regex'} label={'正则表达式'}>
                            <Input/>
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={12}>
                        <Form.Item name={'is_list'} label={'是否列表'} initialValue={false} valuePropName={'checked'}>
                            <Switch/>
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item name={'status'} label={'状态'} initialValue={true} valuePropName={'checked'}>
                            <Switch/>
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
        </Modal>
    )
}

export default RuleModal

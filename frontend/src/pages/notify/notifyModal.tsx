import {Form, Input, Modal, Radio} from "antd";
import {FormModalProps} from "../../utils/useFormModal";
import {notifies} from "../../utils/constants";
import React from "react";
import {NotifyItem} from "./item";

function NotifyModal(props: FormModalProps) {

    const {form, initValues, ...otherProps} = props

    const id = initValues?.id

    return (
        <Modal title={id ? '编辑通知' : '新建通知'} {...otherProps}>
            <Form form={form} layout={'vertical'}>
                <Form.Item name={'name'} label={'名称'} rules={[{required: true, message: '请输入名称'}]}>
                    <Input/>
                </Form.Item>
                <Form.Item name={'type'} label={'类型'} rules={[{required: true}]}
                           initialValue={Object.values(notifies)[0].name}>
                    <Radio.Group>
                        {Object.keys(notifies).map(key => (
                            <Radio key={key} value={key}>
                                <NotifyItem name={notifies[key].description} icon={notifies[key].icon}/>
                            </Radio>
                        ))}
                    </Radio.Group>
                </Form.Item>
                <Form.Item noStyle dependencies={[]}>
                    {({getFieldValue}) => {
                        const type = getFieldValue('type')
                        const Payload = notifies[type].form
                        return (
                            <Payload/>
                        )
                    }}
                </Form.Item>
            </Form>
        </Modal>
    )
}

export default NotifyModal

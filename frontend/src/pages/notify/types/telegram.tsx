import {Form, Input} from "antd";

function NotifyTypeTelegram() {
    return (
        <>
            <Form.Item name={['payload', 'token']} label={'Token'} rules={[{required: true, message: '请输入Token'}]}>
                <Input/>
            </Form.Item>
            <Form.Item name={['payload', 'chat_id']} label={'Chat ID'}
                       rules={[{required: true, message: '请输入Chat ID'}]}>
                <Input/>
            </Form.Item>
        </>
    )
}

export default NotifyTypeTelegram

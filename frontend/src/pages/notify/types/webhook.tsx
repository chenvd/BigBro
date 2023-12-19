import {Form, Input} from "antd";

function NotifyTypeWebhook() {
    return (
        <>
            <Form.Item name={['payload', 'webhook_url']} label={'Webhook URL'} rules={[{required: true, message: '请输入Webhook URL'}]}>
                <Input/>
            </Form.Item>
        </>
    )
}

export default NotifyTypeWebhook

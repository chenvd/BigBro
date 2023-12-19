import {Button, Card, Form, Input, InputNumber} from "antd";

function Setting() {
    return (
        <Card title={'设置'}>
            <div style={{width: 600, maxWidth: '100%', margin: '0 auto'}}>
                <Form layout={'vertical'}>
                    <Form.Item label={'User Agent'} name={'user_agent'}>
                        <Input/>
                    </Form.Item>
                    <Form.Item label={'超时时间(秒)'} name={'timeout'}>
                        <InputNumber style={{width: '100%'}}/>
                    </Form.Item>
                    <Form.Item label={'语言设置'} name={'accept_language'}>
                        <Input/>
                    </Form.Item>
                    <div style={{textAlign: 'center'}}>
                        <Button type={'primary'} style={{width: 150}}>提交</Button>
                    </div>
                </Form>
            </div>
        </Card>
    )
}

export default Setting

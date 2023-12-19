import {Card, Col, FloatButton, message, Row, Skeleton, Space, Tooltip} from "antd";
import {DeleteOutlined, EditOutlined, HistoryOutlined, PlusOutlined, ThunderboltOutlined} from "@ant-design/icons";
import {useRequest} from "ahooks";
import * as api from "../../apis/rule";
import RuleModal from "./ruleModal";
import {useFormModal} from "../../utils/useFormModal";
import React, {useState} from "react";
import {Badge} from "antd/lib";
import HistoryModal from "./historyModal";


function Rule() {

    const {data = [], loading, refresh} = useRequest(async () => (await api.getRules()).data.data)
    const [historyRule, setHistoryRule] = useState<any>()

    const {setOpen, modalProps} = useFormModal({
        service: api.modifyRule,
        onOk: () => {
            message.success("保存成功")
            setOpen(false)
            refresh()
        }
    })

    const {run: onTrigger, loading: onTriggering} = useRequest(api.triggerRule, {
        manual: true,
        onSuccess: () => {
            message.success("执行成功")
        }
    })

    if (loading) {
        return (
            <Card>
                <Skeleton loading={true}/>
            </Card>
        )
    }

    function getOrigin(url: string) {
        return (new URL(url)).origin
    }

    return (
        <Row gutter={[15, 15]}>
            {data.map((item: any) => (
                <Col key={item.id} span={24} lg={8}>
                    <Card actions={[
                        <EditOutlined onClick={() => setOpen(true, item)}/>,
                        <DeleteOutlined/>,
                        <ThunderboltOutlined onClick={() => onTrigger(item.id)}/>,
                        <Badge styles={{root: {color: 'inherit'}}} offset={[5, 0]} dot={item.has_new}><HistoryOutlined
                            onClick={() => {
                                setHistoryRule(item)
                            }}/></Badge>,
                    ]}>
                        <Card.Meta
                            avatar={<img style={{height: 30}} src={item.favicon} alt=""/>}
                            title={item.name}
                            description={(
                                <Space direction={'vertical'}>
                                    <Tooltip title={item.url}>
                                        {getOrigin(item.url)}
                                    </Tooltip>
                                    <div>
                                        {item.lastest_update}
                                    </div>
                                </Space>
                            )}
                        />
                    </Card>
                </Col>
            ))}
            <RuleModal {...modalProps}/>
            <HistoryModal rule={historyRule} open={historyRule} onCancel={() => setHistoryRule(undefined)}/>
            <FloatButton icon={<PlusOutlined/>} type="primary" style={{right: 24}} onClick={() => setOpen(true)}/>
        </Row>
    )
}

export default Rule

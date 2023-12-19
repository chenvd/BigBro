import {Card, List, message} from "antd";
import {notifies} from "../../utils/constants";
import More from "../../components/More";
import {useRequest} from "ahooks";
import * as api from "../../apis/notify";
import {PlusOutlined} from "@ant-design/icons";
import IconButton from "../../components/IconButton";
import React from "react";
import {useFormModal} from "../../utils/useFormModal";
import NotifyModal from "./notifyModal";
import {NotifyItemIcon} from "./item";


function Notify() {

    const {data = [], loading, refresh} = useRequest(async () => {
        const data = (await api.getNotifies()).data.data
        return data.map((i: any) => ({...i, payload: JSON.parse(i.payload)}))
    })

    const {setOpen, modalProps} = useFormModal({
        service: api.modifyNotify,
        onOk: () => {
            message.success("保存成功")
            refresh()
            setOpen(false)
        }
    })

    function onMoreClick(key: string, record: any) {
        if (key === 'edit') {
            setOpen(true, record)
        }
    }

    return (
        <Card title={'通知'} extra={(
            <IconButton onClick={() => setOpen(true)}>
                <PlusOutlined/>
            </IconButton>
        )}>
            <List loading={loading}>
                {data.map((item: any) => (
                    <List.Item key={item.id} actions={[<More onClick={(key) => onMoreClick(key, item)}/>]}>
                        <List.Item.Meta title={item.name}
                                        description={notifies[item.type].name}
                                        avatar={<NotifyItemIcon size={30} icon={notifies[item.type].icon}/>}
                        />
                    </List.Item>
                ))}
            </List>
            <NotifyModal {...modalProps} />
        </Card>
    )
}

export default Notify

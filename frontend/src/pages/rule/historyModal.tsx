import {Modal, ModalProps, Spin, Switch, Timeline} from "antd";
import {useEffect, useState} from "react";
import {useRequest} from "ahooks";
import * as api from "../../apis/rule";
import dayjs from "dayjs";


interface Props extends ModalProps {
    rule?: any
}

function HistoryModal(props: Props) {

    const {rule, ...otherProps} = props
    const [onlyUpdate, setOnlyUpdate] = useState(true)

    const {run, loading, data} = useRequest(async () => {
        const response = (await api.getHistories(rule?.id, onlyUpdate)).data.data
        return response.map((item: any) => ({
            label: dayjs(item.create_time).format('lll'),
            color: ['red', 'blue', 'green'][item.status + 1],
            children: (
                <>
                    <div>{item.content}</div>
                    {item.values?.map((value: any) => (
                        <div>{value.content}({value.groups.split(",").filter((i: string) => !!i)})</div>
                    ))}
                </>
            )
        }))
    }, {
        manual: true,
    })

    useEffect(() => {
        if (props.open) {
            run()
        }
    }, [props.open, onlyUpdate]);

    return (
        <Modal title={'历史记录'} footer={null} {...otherProps}>
            <div style={{display: 'flex', alignItems: 'center', justifyContent: 'right', margin: '15px 0'}}>
                <Switch checked={onlyUpdate} onChange={checked => setOnlyUpdate(checked)}/>
                <span style={{marginLeft: 5}}>仅展示更新</span>
            </div>
            {loading ? (
                <div style={{textAlign: "center"}}><Spin delay={500}/></div>
            ) : (
                <Timeline mode={"left"} items={data}/>
            )}
        </Modal>
    )
}

export default HistoryModal

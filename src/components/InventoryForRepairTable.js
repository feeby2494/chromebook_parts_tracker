import React,{Component, useState} from 'react';
import { ListGroup,Table } from 'react-bootstrap';

const InventoryForRepairTable = (props) => {
//   const [show, setShow] = useState(false);

//   const handleClose = () => setShow(false);
//   const handleShow = () => setShow(true);


  return (
    (props.current_inventories.length > 0) ?
        <>
          <ListGroup.Item as="li" active>
            Inventory for parts
          </ListGroup.Item>
          <Table striped bordered>
            <thead>
              <tr>
                <td>Part Number</td>
                <td>Count</td>
                <td>Location</td>
              </tr>
            </thead>
            {props.current_inventories.map((inventory) => {
              let array = Object.keys(inventory).map((part_name) => {
                let count_name = inventory[part_name]["count"];
                let location_name = inventory[part_name]["location_desc"];
                let part_item_name = part_name;
                  return <tr><td>{part_item_name}</td><td>{count_name}</td><td>{location_name}</td></tr>
                });
              return <tbody>{array}</tbody>
            })}
          </Table>
        </>
        :
          <> </>
    
  );

}

export default InventoryForRepairTable;
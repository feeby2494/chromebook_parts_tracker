import React,{Component, useState} from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const LookUpInventoryByRoom = (props) => {
    return (
        <Row>
            <Col>
                <p>I show all invnentory and some stats for one room. Select the room, then I will show you what you need to know. Useful for double checking inventory by room.</p>
            </Col>
        </Row>

    );
}

export default LookUpInventoryByRoom;
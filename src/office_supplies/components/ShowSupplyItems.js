import React,{Component, useState} from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const ShowSupplyItems = (props) => {
    return (
        <Row>
            <Col>
                <p>I'm a list of all supply items with their invnentory and location code</p>
            </Col>
        </Row>

    );
}

export default ShowSupplyItems;
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Form, Input, Button, Select, message, Card, Typography, Divider, Alert } from 'antd';
import { UserOutlined, PhoneOutlined, MailOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const CustomerServiceRequest = () => {
  const { user, token } = useAuth();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState('');
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    email: '',
    region: '',
    locationDetails: '',
    serviceDescription: '',
    serviceType: '',
    jobBudget: '',
    materialDocuments: []
  });

  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [activeSection, setActiveSection] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;
    
    setIsUploading(true);
    setUploadProgress(0);
    
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    setTimeout(() => {
      setFormData(prev => ({
        ...prev,
        materialDocuments: [...prev.materialDocuments, ...files]
      }));
      clearInterval(interval);
      setIsUploading(false);
      toast.success(`${files.length} file(s) uploaded successfully!`);
    }, 2500);
  };

  const removeFile = (index) => {
    setFormData(prev => ({
      ...prev,
      materialDocuments: prev.materialDocuments.filter((_, i) => i !== index)
    }));
    toast.info('File removed');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    toast.success('Service request submitted successfully!', {
      position: "top-center",
      autoClose: 2500,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      onClose: () => navigate('/customer-dashboard')
    });
    
    console.log('Service Request Submitted:', formData);
  };

  const toggleSection = (section) => {
    setActiveSection(activeSection === section ? null : section);
  };

  const goToDashboard = () => {
    navigate('/customer-dashboard');
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <Card className="shadow-lg">
        <div className="text-center mb-8">
          <Title level={2} className="text-2xl font-bold text-gray-800">
            Customer Support Request
          </Title>
          <Text type="secondary">
            Fill out the form below and our team will get back to you as soon as possible.
          </Text>
        </div>

        {formError && (
          <Alert
            message="Error"
            description={formError}
            type="error"
            showIcon
            className="mb-6"
            closable
            onClose={() => setFormError('')}
          />
        )}

        <Divider orientation="left" className="text-gray-500">
          Contact Information
        </Divider>

        <Form
          form={form}
          name="customerServiceForm"
          layout="vertical"
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
          className="space-y-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Form.Item
              label="Full Name"
              name="name"
              rules={[{ required: true, message: 'Please input your full name!' }]}
            >
              <Input 
                prefix={<UserOutlined className="text-gray-400" />} 
                placeholder="John Doe"
                disabled={!!user?.name}
              />
            </Form.Item>

            <Form.Item
              label="Email"
              name="email"
              rules={[
                { required: true, message: 'Please input your email!' },
                { type: 'email', message: 'Please enter a valid email address' },
              ]}
            >
              <Input 
                prefix={<MailOutlined className="text-gray-400" />} 
                placeholder="your.email@example.com"
                disabled={!!user?.email}
              />
            </Form.Item>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Form.Item
              label="Phone Number"
              name="phone"
              rules={[
                { required: true, message: 'Please input your phone number!' },
                {
                  pattern: /^[0-9\+\-\s\(\)]{10,20}$/,
                  message: 'Please enter a valid phone number!',
                },
              ]}
            >
              <Input 
                prefix={<PhoneOutlined className="text-gray-400" />} 
                placeholder="+254 700 000000"
                disabled={!!user?.phone}
              />
            </Form.Item>

            <Form.Item
              label="Category"
              name="category"
              rules={[{ required: true, message: 'Please select a category!' }]}
            >
              <Select
                placeholder="Select a category"
                allowClear
              >
                {serviceCategories.map(category => (
                  <Option key={category} value={category}>
                    {category}
                  </Option>
                ))}
              </Select>
            </Form.Item>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Form.Item
              label="Priority"
              name="priority"
              initialValue="medium"
              rules={[{ required: true }]}
            >
              <Select>
                {priorityLevels.map(level => (
                  <Option key={level.value} value={level.value}>
                    {level.label}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item
              label="Subject"
              name="subject"
              rules={[{ required: true, message: 'Please input a subject!' }]}
            >
              <Input placeholder="Briefly describe your issue" />
            </Form.Item>
          </div>

          <Form.Item
            label="Description"
            name="description"
            rules={[
              { required: true, message: 'Please provide a detailed description!' },
              { min: 20, message: 'Description must be at least 20 characters long' },
            ]}
          >
            <TextArea
              rows={6}
              placeholder="Please provide as much detail as possible about your issue or question..."
              showCount
              maxLength={2000}
            />
          </Form.Item>

          <Form.Item
            name="attachments"
            label="Attachments"
            extra="Upload any relevant files or screenshots (max 5MB)"
          >
            <Input type="file" multiple />
          </Form.Item>

          <div className="flex items-center text-sm text-gray-500 mb-4">
            <InfoCircleOutlined className="mr-2" />
            <span>We'll respond to your inquiry within 24-48 hours.</span>
          </div>

          <Form.Item className="text-center">
            <Button 
              type="primary" 
              htmlType="submit" 
              size="large"
              loading={loading}
              className="w-full md:w-1/3 bg-blue-600 hover:bg-blue-700 border-none h-12 text-base"
            >
              Submit Request
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default CustomerServiceRequest;




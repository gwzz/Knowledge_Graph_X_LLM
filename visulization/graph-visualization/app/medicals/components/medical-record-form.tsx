'use client';

import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Switch } from './ui/switch';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { AlertTriangle, Save, X } from 'lucide-react';
import { MedicalRecord } from '@/app/medicals/types/medical-record';
import { ApiError } from '@/app/lib/api';

interface MedicalRecordFormProps {
  record?: MedicalRecord | null;
  onSave: (data: Omit<MedicalRecord, 'id'>) => Promise<void>;
  onCancel: () => void;
}

export function MedicalRecordForm({ record, onSave, onCancel }: MedicalRecordFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    describes: '',
    symptom: '',
    seek_medical_attention_immediately: 0,
    follow_up: 0,
    follow_up_describe: '',
    type_ab: '',
    is_emergency: 0,
    urgency_level: 1,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [nameError, setNameError] = useState<string | null>(null);

  useEffect(() => {
    if (record) {
      setFormData({
        name: record.name || '',
        describes: record.describes || '',
        symptom: record.symptom || '',
        seek_medical_attention_immediately: record.seek_medical_attention_immediately || 0,
        follow_up: record.follow_up || 0,
        follow_up_describe: record.follow_up_describe || '',
        type_ab: record.type_ab || '',
        is_emergency: record.is_emergency || 0,
        urgency_level: record.urgency_level || 1,
      });
    }
  }, [record]);

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear name error when user starts typing
    if (field === 'name' && nameError) {
      setNameError(null);
    }
  };

  const handleSwitchChange = (field: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: checked ? 1 : 0
    }));
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setNameError('Patient name is required');
      return false;
    }
    setNameError(null);
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Clean up empty strings to undefined for optional fields
      const cleanedData = {
        ...formData,
        describes: formData.describes.trim() || undefined,
        symptom: formData.symptom.trim() || undefined,
        follow_up_describe: formData.follow_up_describe.trim() || undefined,
        type_ab: formData.type_ab.trim() || undefined,
      };

      await onSave(cleanedData);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to save record');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <Alert className="border-red-200 bg-red-50">
          <AlertTriangle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">
            {error}
          </AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Basic Information</CardTitle>
            <CardDescription>Primary patient and condition details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="name" className="text-sm font-medium">
                Patient Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="Enter patient name"
                className={nameError ? 'border-red-500' : ''}
              />
              {nameError && (
                <p className="text-sm text-red-600 mt-1">{nameError}</p>
              )}
            </div>

            <div>
              <Label htmlFor="describes" className="text-sm font-medium">
                Description
              </Label>
              <Textarea
                id="describes"
                value={formData.describes}
                onChange={(e) => handleInputChange('describes', e.target.value)}
                placeholder="Enter condition description"
                rows={3}
              />
            </div>

            <div>
              <Label htmlFor="type_ab" className="text-sm font-medium">
                Type Classification
              </Label>
              <Input
                id="type_ab"
                value={formData.type_ab}
                onChange={(e) => handleInputChange('type_ab', e.target.value)}
                placeholder="Enter type classification (e.g., Type A, Type B)"
              />
            </div>
          </CardContent>
        </Card>

        {/* Symptoms */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Symptoms</CardTitle>
            <CardDescription>Patient symptoms and observations</CardDescription>
          </CardHeader>
          <CardContent>
            <div>
              <Label htmlFor="symptom" className="text-sm font-medium">
                Symptoms
              </Label>
              <Textarea
                id="symptom"
                value={formData.symptom}
                onChange={(e) => handleInputChange('symptom', e.target.value)}
                placeholder="Describe patient symptoms"
                rows={4}
              />
            </div>
          </CardContent>
        </Card>

        {/* Medical Urgency */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Medical Urgency</CardTitle>
            <CardDescription>Emergency status and urgency levels</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">Emergency Case</Label>
                <p className="text-sm text-gray-500">Is this an emergency situation?</p>
              </div>
              <Switch
                checked={formData.is_emergency === 1}
                onCheckedChange={(checked: boolean) => handleSwitchChange('is_emergency', checked)}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">Immediate Medical Attention</Label>
                <p className="text-sm text-gray-500">Requires immediate care?</p>
              </div>
              <Switch
                checked={formData.seek_medical_attention_immediately === 1}
                onCheckedChange={(checked: boolean) => handleSwitchChange('seek_medical_attention_immediately', checked)}
              />
            </div>

            <div>
              <Label htmlFor="urgency_level" className="text-sm font-medium">
                Urgency Level
              </Label>
              <Select
                value={formData.urgency_level.toString()}
                onValueChange={(value:string) => handleInputChange('urgency_level', parseInt(value))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select urgency level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">Level 1 - Low</SelectItem>
                  <SelectItem value="2">Level 2 - Medium</SelectItem>
                  <SelectItem value="3">Level 3 - High</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Follow-up */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Follow-up Care</CardTitle>
            <CardDescription>Follow-up requirements and details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">Requires Follow-up</Label>
                <p className="text-sm text-gray-500">Does this case need follow-up care?</p>
              </div>
              <Switch
                checked={formData.follow_up === 1}
                onCheckedChange={(checked: boolean) => handleSwitchChange('follow_up', checked)}
              />
            </div>

            {formData.follow_up === 1 && (
              <div>
                <Label htmlFor="follow_up_describe" className="text-sm font-medium">
                  Follow-up Description
                </Label>
                <Textarea
                  id="follow_up_describe"
                  value={formData.follow_up_describe}
                  onChange={(e) => handleInputChange('follow_up_describe', e.target.value)}
                  placeholder="Describe follow-up requirements"
                  rows={3}
                />
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button
          type="button"
          onClick={onCancel}
          disabled={loading}
        >
          <X className="h-4 w-4 mr-2" />
          Cancel
        </Button>
        <Button 
          type="submit" 
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <Save className="h-4 w-4 mr-2" />
          {loading ? 'Saving...' : 'Save Record'}
        </Button>
      </div>
    </form>
  );
}
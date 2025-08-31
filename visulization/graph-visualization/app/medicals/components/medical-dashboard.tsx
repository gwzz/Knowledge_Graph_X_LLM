'use client';

import React, { useState, useEffect } from 'react';
import { Plus, Search, Filter, Edit2, Trash2, AlertTriangle, Clock, User } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Alert, AlertDescription } from './ui/alert';
import { MedicalRecord } from '../types/medical-record';
import { api, ApiError } from '@/app/lib/api';
import { MedicalRecordForm } from './medical-record-form';
import { DeleteConfirmDialog } from './delete-confirm-dialog';

export function MedicalDashboard() {
  const [records, setRecords] = useState<MedicalRecord[]>([]);
  const [filteredRecords, setFilteredRecords] = useState<MedicalRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRecord, setSelectedRecord] = useState<MedicalRecord | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [recordToDelete, setRecordToDelete] = useState<MedicalRecord | null>(null);

  useEffect(() => {
    fetchRecords();
  }, []);

  useEffect(() => {
    const filtered = records.filter(record =>
      record.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.describes?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.symptom?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.type_ab?.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredRecords(filtered);
  }, [records, searchTerm]);

  const fetchRecords = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getAllRecords();
      setRecords(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to fetch records');
      setRecords([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveRecord = async (recordData: Omit<MedicalRecord, 'id'>) => {
    try {
      if (selectedRecord) {
        await api.updateRecord(selectedRecord.id!, recordData);
      } else {
        await api.createRecord(recordData);
      }
      await fetchRecords();
      setIsFormOpen(false);
      setSelectedRecord(null);
    } catch (err) {
      throw err;
    }
  };

  const handleDeleteRecord = async () => {
    if (!recordToDelete) return;
    
    try {
      await api.deleteRecord(recordToDelete.id!);
      await fetchRecords();
      setIsDeleteOpen(false);
      setRecordToDelete(null);
    } catch (err) {
      console.error('Failed to delete record:', err);
    }
  };

  const openCreateForm = () => {
    setSelectedRecord(null);
    setIsFormOpen(true);
  };

  const openEditForm = (record: MedicalRecord) => {
    setSelectedRecord(record);
    setIsFormOpen(true);
  };

  const openDeleteDialog = (record: MedicalRecord) => {
    setRecordToDelete(record);
    setIsDeleteOpen(true);
  };

  const getUrgencyBadge = (level?: number) => {
    if (!level) return null;
    
    const variants: { [key: number]: 'default' | 'secondary' | 'destructive' | 'outline' } = {
      1: 'default',
      2: 'secondary', 
      3: 'destructive'
    };
    
    const labels = {
      1: 'Low',
      2: 'Medium', 
      3: 'High'
    };
    
    return (
      <Badge variant={variants[level] || 'outline'}>
        {labels[level] || `Level ${level}`}
      </Badge>
    );
  };

  const getEmergencyBadge = (isEmergency?: number) => {
    if (!isEmergency) return null;
    return (
      <Badge variant="destructive" className="flex items-center gap-1">
        <AlertTriangle className="h-3 w-3" />
        Emergency
      </Badge>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading medical records...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <User className="h-8 w-8 text-blue-600" />
            Medical Records Dashboard
          </h1>
          <p className="mt-2 text-gray-600">Manage patient medical records and conditions</p>
        </div>

        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        <Card className="mb-6">
          <CardHeader>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  Records Overview
                </CardTitle>
                <CardDescription>
                  {filteredRecords.length} of {records.length} records
                </CardDescription>
              </div>
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Search records..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 w-full sm:w-64"
                  />
                </div>
                <Button onClick={openCreateForm} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Record
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Patient Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Emergency</TableHead>
                    <TableHead>Urgency</TableHead>
                    <TableHead>Follow-up</TableHead>
                    <TableHead>Immediate Care</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredRecords.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} className="text-center py-8">
                        <div className="text-gray-500">
                          <User className="h-12 w-12 mx-auto mb-2 opacity-50" />
                          {searchTerm ? 'No records match your search' : 'No medical records found'}
                        </div>
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredRecords.map((record) => (
                      <TableRow key={record.id} className="hover:bg-gray-50">
                        <TableCell>
                          <div>
                            <div className="font-medium text-gray-900">{record.name}</div>
                            {record.describes && (
                              <div className="text-sm text-gray-500 truncate max-w-xs">
                                {record.describes}
                              </div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          {record.type_ab && (
                            <Badge variant="outline">{record.type_ab}</Badge>
                          )}
                        </TableCell>
                        <TableCell>
                          {getEmergencyBadge(record.is_emergency)}
                        </TableCell>
                        <TableCell>
                          {getUrgencyBadge(record.urgency_level)}
                        </TableCell>
                        <TableCell>
                          {record.follow_up ? (
                            <Badge variant="secondary" className="flex items-center gap-1 w-fit">
                              <Clock className="h-3 w-3" />
                              Required
                            </Badge>
                          ) : (
                            <span className="text-gray-400">No</span>
                          )}
                        </TableCell>
                        <TableCell>
                          {record.seek_medical_attention_immediately ? (
                            <Badge variant="destructive">Yes</Badge>
                          ) : (
                            <span className="text-gray-400">No</span>
                          )}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => openEditForm(record)}
                            >
                              <Edit2 className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => openDeleteDialog(record)}
                              className="text-red-600 hover:text-red-700 hover:bg-red-50"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {selectedRecord ? 'Edit Medical Record' : 'Create Medical Record'}
              </DialogTitle>
            </DialogHeader>
            <MedicalRecordForm
              record={selectedRecord}
              onSave={handleSaveRecord}
              onCancel={() => setIsFormOpen(false)}
            />
          </DialogContent>
        </Dialog>

        <DeleteConfirmDialog
          open={isDeleteOpen}
          onOpenChange={setIsDeleteOpen}
          onConfirm={handleDeleteRecord}
          recordName={recordToDelete?.name || ''}
        />
      </div>
    </div>
  );
}
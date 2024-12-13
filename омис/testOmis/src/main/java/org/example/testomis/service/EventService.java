package org.example.testomis.service;

import org.example.testomis.payload.request.EventRequest;
import org.example.testomis.payload.response.EventResponse;
import org.example.testomis.payload.response.FileResponse;
import org.springframework.web.multipart.MultipartFile;

import java.security.Principal;
import java.util.List;

public interface EventService {

    EventResponse create(EventRequest request, Principal principal);

    EventResponse update(long id, EventRequest request, Principal principal);

    void delete(long id, Principal principal);

    EventResponse getById(long id, Principal principal);

    List<EventResponse> getAll(Principal principal);

    List<EventResponse> getAllNew(Principal principal);

    List<EventResponse> getAllPast(Principal principal);

    void addFile(long id, MultipartFile file, Principal principal);

    byte[] getFile(long id, Principal principal);
}

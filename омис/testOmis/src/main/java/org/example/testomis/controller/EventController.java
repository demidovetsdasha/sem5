package org.example.testomis.controller;

import lombok.RequiredArgsConstructor;
import org.example.testomis.payload.request.EventRequest;
import org.example.testomis.payload.response.EventResponse;
import org.example.testomis.payload.response.FileResponse;
import org.example.testomis.service.EventService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.security.Principal;
import java.util.List;

@RestController
@RequestMapping("/api/events")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:4200", methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE, RequestMethod.OPTIONS})
public class EventController {

    private final EventService eventService;

    @GetMapping("/new")
    public ResponseEntity<List<EventResponse>> getAllNew(Principal principal){
        return ResponseEntity.ok(eventService.getAllNew(principal));
    }

    @GetMapping("/past")
    public ResponseEntity<List<EventResponse>> getAllPast(Principal principal){
        return ResponseEntity.ok(eventService.getAllPast(principal));
    }

    @GetMapping("/{id}")
    public ResponseEntity<EventResponse> getById(
            @PathVariable long id,
            Principal principal
    ){
        return ResponseEntity.ok()
                .body(eventService.getById(id, principal));
    }

    @PutMapping("/file/{id}")
    public ResponseEntity<Void> addFile(
            @PathVariable long id,
            MultipartFile file,
            Principal principal
    ){
        eventService.addFile(id, file, principal);

        return ResponseEntity.noContent().build();
    }

    @GetMapping("/file/get/{id}")
    public ResponseEntity<byte[]> getFile(
            @PathVariable long id,
            Principal principal
    ){
        var gettedFile = eventService.getFile(id, principal);

        if(gettedFile == null){
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok()
                .body(gettedFile);
    }

    @PutMapping("/{id}")
    public ResponseEntity<EventResponse> update(
            @PathVariable long id,
            @RequestBody EventRequest request,
            Principal principal
    ){
        return ResponseEntity.ok()
                .body(eventService.update(id, request, principal));
    }

    @PostMapping
    public ResponseEntity<EventResponse> create(
            @RequestBody EventRequest request,
            Principal principal
    ) {
        return ResponseEntity.status(201)
                .body(eventService.create(request, principal));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id,
                                       Principal principal) {
        eventService.delete(id, principal);
        return ResponseEntity.noContent().build();
    }

}

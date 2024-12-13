package org.example.testomis.service.impl;

import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.example.testomis.error.UsernameNotFoundException;
import org.example.testomis.model.Event;
import org.example.testomis.model.PresentationData;
import org.example.testomis.model.User;
import org.example.testomis.model.enums.EventCategory;
import org.example.testomis.payload.request.EventRequest;
import org.example.testomis.payload.response.EventResponse;
import org.example.testomis.payload.response.FileResponse;
import org.example.testomis.repository.EventRepository;
import org.example.testomis.repository.UserRepository;
import org.example.testomis.service.EventService;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.security.Principal;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class EventServiceImpl implements EventService {

    private final EventRepository eventRepository;
    private final UserRepository userRepository;

    @Override
    public EventResponse create(EventRequest request, Principal principal) {
        var event = convert(request, principal);
        eventRepository.save(event);
        return convert(event);
    }

    @Override
    public EventResponse update(long id, EventRequest request, Principal principal) {
        var event = convert(request, principal);
        event.setId(id);
        eventRepository.save(event);
        return convert(event);
    }

    @Override
    public void delete(long id, Principal principal) {
        if (principal == null) {
            throw new RuntimeException("User is not authenticated");
        }

        Event event = eventRepository
                .findByIdAndUser(id, getUserByPrincipal(principal))
                .orElseThrow(RuntimeException::new);

        eventRepository.delete(event);
    }

    @Override
    public EventResponse getById(long id, Principal principal) {
        return convert(eventRepository.findByIdAndUser(id, getUserByPrincipal(principal))
                .orElseThrow(RuntimeException::new));
    }

    @Override
    public List<EventResponse> getAll(Principal principal) {
        var user = getUserByPrincipal(principal);
        return eventRepository.findByUser(user).stream()
                .map(this::convert)
                .collect(Collectors.toList());
    }

    @Override
    public List<EventResponse> getAllNew(Principal principal) {
        var user = getUserByPrincipal(principal);
        var currentDate = new Date(); // Получаем текущую дату и время
        return eventRepository.findByUser(user).stream()
                .filter(event -> event.getFinish().after(currentDate)) // Фильтруем по endTime
                .map(this::convert)
                .collect(Collectors.toList());
    }

    @Override
    public List<EventResponse> getAllPast(Principal principal) {
        var user = getUserByPrincipal(principal);
        var currentDate = new Date(); // Получаем текущую дату и время
        return eventRepository.findByUser(user).stream()
                .filter(event -> event.getFinish().before(currentDate)) // Фильтруем по endTime
                .map(this::convert)
                .collect(Collectors.toList());
    }

    @SneakyThrows
    @Override
    public void addFile(long id, MultipartFile file, Principal principal) {
        Event event = eventRepository.findByIdAndUser(id, getUserByPrincipal(principal))
                .orElseThrow(RuntimeException::new);

        PresentationData presentationData = new PresentationData();

        presentationData.setOriginalName(file.getOriginalFilename());
        presentationData.setFile(file.getBytes());
        presentationData.setDate(new Date());

        event.setFile(presentationData);
        eventRepository.save(event);
    }

    @Override
    public byte[] getFile(long id, Principal principal) {
        Event event = eventRepository.findByIdAndUser(id, getUserByPrincipal(principal))
                .orElseThrow(RuntimeException::new);

        if(event.getFile() == null) {
            return null;
        }

        return event.getFile().getFile();
    }

    private Event convert(EventRequest request, Principal principal){
        var event = new Event();
        var user = getUserByPrincipal(principal);
        event.setAuthor(request.author());
        event.setUser(user);
        event.setName(request.name());
        event.setCategory(EventCategory.valueOf(request.category()));
        event.setStart(convertStringToDate(request.start()));
        event.setFinish(convertStringToDate(request.finish()));
        return event;
    }

    @SneakyThrows
    private Date convertStringToDate(String stringDate){
        SimpleDateFormat formatterWithTime = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return formatterWithTime.parse(stringDate);
    }

    private EventResponse convert(Event event){
       return EventResponse.builder()
               .id(Math.toIntExact(event.getId()))
               .author(event.getAuthor())
               .category(String.valueOf(event.getCategory()))
               .start(String.valueOf(event.getStart()))
               .finish(String.valueOf(event.getFinish()))
               .name(event.getName())
               .build();
    }

    private User getUserByPrincipal(Principal principal){
        return userRepository.findByUsernameIgnoreCase(principal.getName())
                .orElseThrow(() -> new UsernameNotFoundException("User " + principal.getName() + " not found"));
    }
}
